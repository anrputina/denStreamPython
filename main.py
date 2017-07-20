#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:04:57 2017

@author: anr.putina
"""

import time as tm
import pandas as pd
from point import Point
from DenStream import DenStream
from denDBScan import denDBScan
from groundTruth import groundTruth

from statistics import statistics
from visualization import Visualization

import matplotlib.pyplot as plt
from microCluster import MicroCluster
from sklearn.neighbors import NearestNeighbors

def normalize_matrix(df):
    return (df - df.mean())/df.std()

import numpy as np
### PREPARE DATA

startingSimulation = tm.time()



samplesConsidered = 500
sampleSkip = 60

#### ground truth ###

truth = groundTruth()
truth.simulationBGP_CLEAR3()

#############################

resultSimulation = {}

nodeSimulationList = ['leaf1', 'leaf2', 'leaf3', 'leaf5', 'leaf6', 'leaf7', 'leaf8',
                      'spine1', 'spine2', 'spine3', 'spine4']

#nodeSimulationList = ['leaf8']

for node in nodeSimulationList:
    
    print node
    
    df = pd.read_csv(node+'_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)

    df['time'] = df['time'] / 1000000

    time = df['time']
    time = time[:samplesConsidered]

    df = df.drop(['time'], axis=1)
    df = df[:samplesConsidered]

    dfNormalized = normalize_matrix(df).dropna(axis=1)

    bufferDf = dfNormalized[10:sampleSkip]
    testDf = dfNormalized[sampleSkip:]


    den = DenStream(horizon=150, epsilon=10, minPoints=5, beta=0.2, mu=6, initPointOption=2, startingPoints=bufferDf)
    den.setHistory(True)
####
    den.runInitialization()
#######
#    simulationTime = []

#    counter = 0
    for sampleNumber in range(len(testDf)):
    #for sampleNumber in range(1,8):
    #    print counter
#        start = tm.time()
        sample = testDf.iloc[sampleNumber]
        den.runOnNewPoint(Point(sample.values, time.iloc[sampleNumber]))
#        end = tm.time()
#        simulationTime.append(end-start)
    #    counter += 1
    


#    visual = Visualization()
#    
#    result = den.history
#    outliers = []
#    merged = []
#    for event in result:
#        
#        if event['event'] == 'Outlier':
#            outliers.append(event)
#            
#        if event['event'] == 'Merged':
#            merged.append(event)
#            
#    #features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received', 'HundredGigE0/0/0/0packets-sent']        
#    features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received']        
#    #visual.plotOutliers(features, df, outliers, merged, truth, sampleSkip-1)
#    #visual.plotOutliersInteractive(features, df, outliers, merged, truth, sampleSkip-1)
#    visual.plotOutliersInteractiveTimestamp(features, df, outliers, merged, truth, sampleSkip-1, time=time)
#
##    visual.plotHistTimeDifference([df, df4])



#    ### label ###
#    result = time < 1
#    df['labels'] = ['clear'] * len(time)
#    for event in truth.events:
#        
#        check = (time >= event['startTime']) & (time <= event['endTime'])
#    
#        df['labels'].loc[check] = event['name']
#    
#        result = result | check
#    
#    df['outlier'] = result 
    
    
    ### outputs ###
    output = [False] * sampleSkip
    result = den.history
    for  event in result:
        
        if event['event'] == 'Outlier':
            output.append(True)
        if event['event'] == 'Merged':
            output.append(False)
    
    df['result'] = output
    #

    stats = statistics(node)
    
    probabilityDetection = stats.findProbabilityDetection(df, truth, time)
    delay = stats.findDelayDetection(df, truth, time)

    resultSimulation[node] = {
            'pDetection': probabilityDetection,
            'delay': delay
          }
    
endingSimulation = tm.time()


#### DELAYS ###
delays = np.zeros(shape=(5,3))
#delays[:] = np.inf
counters = np.zeros(shape=(5,3))

for key, value in resultSimulation.iteritems():
    
    for k in range(1, 6):
        
        for depth in range(3):
            
            if (value['delay'][k][depth] != np.inf):
                
#                if value['delay'][k][depth] < delays[k-1][depth]:
#                    delays[k-1][depth] = value['delay'][k][depth]

                delays[k-1][depth] += value['delay'][k][depth]
                counters[k-1][depth] += 1
            
resultsDivided = np.divide(delays, counters)         


fig, ax= plt.subplots(figsize=(6,6))
for k in range(4):
    ax.plot([0, 1, 2], np.divide(resultsDivided[k], 1000.), label='delay#K' + str(k+1))
    
ax.set_xlabel('#hops')
ax.set_ylabel('detection delay [s]')

plt.xticks([0,1,2], [0,1,2], rotation='horizontal')

# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
          fancybox=True, shadow=True, ncol=5)

#ax.axis([0, 2, 0, 35])
ax.grid()

ax.set_title('Min delay')

#plt.savefig('minDelay.png',bbox_inches='tight')


### p detection ###
pDetections = np.zeros(shape=(5,3))
countersDetections = np.zeros(shape=(5,3))

for key, value in resultSimulation.iteritems():
    
    for k in range(1, 6):
        
        for depth in range(3):
            
            if (value['pDetection'][k][depth] != -1):
            
                pDetections[k-1][depth] += value['pDetection'][k][depth]
                countersDetections[k-1][depth] += 1
            
resultsDivided = np.divide(pDetections, countersDetections)   


fig, ax = plt.subplots(figsize=(6,6))

for k in range(4):
    
    if k == 3:
        ax.plot([0,1,2], resultsDivided[k], label='detection#K'+str(k+1), linestyle='--', linewidth=2.0, color='black')
    else:
        ax.plot([0,1,2], resultsDivided[k], label='detection#K'+str(k+1))


ax.set_xlabel('#hops')
ax.set_ylabel('detection probability [p]')
plt.xticks([0,1,2], [0,1,2], rotation='horizontal')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
          fancybox=True, shadow=True, ncol=5)

ax.axis([0, 2, 0, 1.1])
ax.grid()

ax.set_title('Detection Probability')
#plt.savefig("probabilityDetection.png", bbox_inches='tight')











