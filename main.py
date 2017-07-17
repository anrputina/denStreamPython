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
#df = pd.read_csv('leaf1_5min.csv').dropna().drop('Unnamed: 0', axis=1)
df = pd.read_csv('leaf1_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf2clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('spine4_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf8_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('spine2_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('dr01_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('dr01_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('spine3_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf3_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf6_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf7_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf8_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf5_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('spine1_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)


time = df['time']

#epoch = df['epoch']
df = df.drop(['time'], axis=1)
df = df[:500]

dfNormalized = normalize_matrix(df).dropna(axis=1)
#dfNormalized = df

sampleSkip = 60

bufferDf = dfNormalized[10:sampleSkip]
testDf = dfNormalized[sampleSkip:]


### Neighbors ### 

#dataset = normalize_matrix(bufferDf).dropna(axis=1)
##dataset = bufferDf
#neigh = NearestNeighbors()
#neigh.fit(dataset) 
#prova = neigh.kneighbors(dataset, 20, return_distance=True)
#
#lista = pd.DataFrame()
#dist = pd.DataFrame(prova[0]).drop(0, axis=1)
#for row in range(1, dist.shape[1]+1):
#    lista = pd.concat([lista, dist[row]], ignore_index=True)
#
#plt.plot(lista.sort_values(0).values)



### DENSTREAM INITIALIZATION ### 
#bufferInit = []
#for sampleNumber in range(len(bufferDf)):
#    sample = Point(bufferDf.iloc[sampleNumber].tolist())
#    bufferInit.append(sample)
#

#from sklearn.cluster import DBSCAN
#db = DBSCAN(eps=15, min_samples=5, algorithm='brute').fit(bufferDf)
#a = db.labels_
##
#
#
#den = DenStream(horizon=150, epsilon=5, minPoints=4, beta=0.2, mu=10, initPointOption=2, startingPoints=bufferInit)
#den = DenStream(horizon=150, epsilon=2.5, minPoints=5, beta=0.2, mu=10, initPointOption=2, startingPoints=bufferDf)
den = DenStream(horizon=150, epsilon=10, minPoints=5, beta=0.2, mu=10, initPointOption=2, startingPoints=bufferDf)
den.setHistory(True)
####
den.runInitialization()
#######
simulationTime = []

for sampleNumber in range(len(testDf)):
#for sampleNumber in range(1,8):
    start = tm.time()
    sample = testDf.iloc[sampleNumber]
    den.runOnNewPoint(Point(sample.values, time.iloc[sampleNumber]))
    end = tm.time()
    simulationTime.append(end-start)
    
#### ground truth times ###

truth = groundTruth()
truth.simulationBGP_CLEAR()

#############################

visual = Visualization()

result = den.history
outliers = []
merged = []
for event in result:
    
    if event['event'] == 'Outlier':
        outliers.append(event)
        
    if event['event'] == 'Merged':
        merged.append(event['time'])
        
#features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received', 'HundredGigE0/0/0/0packets-sent']        
features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received']        
#visual.plotOutliers(features, df, outliers, merged, truth, sampleSkip-1)
visual.plotOutliersInteractive(features, df, outliers, merged, truth, sampleSkip-1)

#features = ['paths-count', '0/RP0/CPU0free-application-memory']
#fig, ax = plt.subplots(2)
#plotNumber = 0
#for feature in features:
#    ax[plotNumber].plot(df[feature])
#    
#    for outlier in outliers:
#        ax[plotNumber].plot(outlier['time']+sampleSkip, df.iloc[outlier['time']+sampleSkip-1][feature], color='r', marker='o')
#    
#    plotNumber += 1

### label ###
time = time[:500]
result = time < 1
df['labels'] = ['clear'] * len(time)
for event in truth.events:
    
    check = (time >= event['startTime']) & (time <= event['endTime'])

    df['labels'].loc[check] = event['name']

    result = result | check

df['outlier'] = result 


### outputs ###
output = [False] * 60
result = den.history
for  event in result:
    
    if event['event'] == 'Outlier':
        output.append(True)
    if event['event'] == 'Merged':
        output.append(False)

df['result'] = output
#
tp = (df['outlier'] == True) & (df['result'] == True)
tn = (df['outlier'] == False) & (df['result'] == False)

fp = (df['outlier'] == False) & (df['result'] == True)
fn = (df['outlier'] == True) & (df['result'] == False)

precision = tp.sum() / float((tp.sum() + fp.sum()))
recall = tp.sum() / float((tp.sum() + fn.sum()))




#for event in truth.events:
#    
##    check = (time >= event['startTime']) & (time <= event['endTime'])
#
#    detection = df['result'][(time >= event['startTime']) & (time <= event['endTime'])]
#    
#    if detection > 0:
#        tp2 += 1
#    else:
#        fn2 += 1
#    
#    detection = df['result']
#    
#    
#    print detection.sum()

tp2 = 0
tn2 = 0
fn2 = 0
fp2 = 0


for eventNumber in range(len(truth.events)):
    
    event = truth.events[eventNumber]
    
    detection = df['result'][(time >= event['startTime']) & (time <= event['endTime'])]
    
    if detection.sum() > 0:
        tp2 += 1
    else:
        fn2 += 1  
        
    if eventNumber != len(truth.events) -1 :
        detectionClear = df['result'][(time > event['endTime']) & (time < truth.events[eventNumber+1]['startTime'])]
    else:
        detectionClear = df['result'][(time > event['endTime'])]
        
    if detectionClear.sum() > 0 :
        fp2 += 1
    else:
        tn2 += 1
        
precision = tp2/(float(tp2+fp2))
recall = tp2/(float(tp2+fn2))



pDetection1 = [0] * 3
pDetection2 = [0] * 3
pDetection3 = [0] * 3


node='leaf1'
stats = statistics(node)

boh = stats.findProbabilityDetection(df, truth)
delay = stats.findDelayDetection(df, truth)

plt.figure()
for key, value in boh.iteritems():
    plt.plot(value, label=key, color='r')
#plt.legend()
#plt.axis([0,2,0,1.1])

for key, value in delay.iteritems():
    plt.plot(value, label=key, marker='x', color='g')
#    plt.plot(np.divide(value, float(max(value))), label=key, marker='x', color='g')
#plt.legend(loc=4)
#plt.axis([0,2,0,1.1])