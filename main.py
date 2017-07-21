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

from multiprocessing import Process

def normalize_matrix(df):
    return (df - df.mean())/df.std()

import os
import errno
import json

import numpy as np
### PREPARE DATA




samplesConsidered = 500
sampleSkip = 60

#### ground truth ###

truth = groundTruth()
truth.simulationBGP_CLEAR3()

#############################

nodeSimulationList = ['leaf1', 'leaf2', 'leaf3', 'leaf5', 'leaf6', 'leaf7', 'leaf8',
                      'spine1', 'spine2', 'spine3', 'spine4']

#nodeSimulationList = ['leaf8']

def worker(node):
        
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
    
    filename = "./Results/"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
                
    out_file = open(filename+node+'.csv',"w")
    row = 'node, epsilon, lambda, beta, mu'
    
    for k in range(5):
        
        for depth in range(3):
                        
            row = row + 'pdetectk' + str(k) + 'd' + str(depth) + ','
    
    row = row + 'duration\n'
    out_file.write(row)
    
    lambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    betas = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    mus = [6, 8, 10, 12, 14, 16, 18, 20]
    epsilons = [6, 8, 10, 12, 14, 16, 18, 20]
    
#    lambdas = [0.5]
#    betas = [0.2]
#    mus = [8]
    
    for lamb in lambdas:
        for beta in betas:
            for mu in mus:
                for epsilon in epsilons:
                    
                
                    ### START SIMULATION ###
                    startingSimulation = tm.time()
                    den = DenStream(epsilon=epsilon, lamb=lamb, minPoints=5, beta=beta, mu=mu, initPointOption=2, startingPoints=bufferDf)
                    den.setHistory(True)
                    den.runInitialization()
                    
                    for sampleNumber in range(len(testDf)):
                        sample = testDf.iloc[sampleNumber]
                        den.runOnNewPoint(Point(sample.values, time.iloc[sampleNumber]))
                    endingSimulation = tm.time()
                    ### END SIMULATION ###
                        
                    ### outputs ###
                    output = [False] * sampleSkip
                    result = den.history
                    for  event in result:
                        
                        if event['event'] == 'Outlier':
                            output.append(True)
                        if event['event'] == 'Merged':
                            output.append(False)
                    
                    df['result'] = output
                    
                    stats = statistics(node)
                    probabilityDetection = stats.findProbabilityDetection(df, truth, time)
                    delay = stats.findDelayDetection(df, truth, time)
                    
        #            visual = Visualization()
        #            
        #            result = den.history
        #            outliers = []
        #            merged = []
        #            for event in result:
        #                
        #                if event['event'] == 'Outlier':
        #                    outliers.append(event)
        #                    
        #                if event['event'] == 'Merged':
        #                    merged.append(event)
        #                    
        #            #features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received', 'HundredGigE0/0/0/0packets-sent']        
        #            features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received']        
        #            #visual.plotOutliers(features, df, outliers, merged, truth, sampleSkip-1)
        #            #visual.plotOutliersInteractive(features, df, outliers, merged, truth, sampleSkip-1)
        #            visual.plotOutliersInteractiveTimestamp(features, df, outliers, merged, truth, sampleSkip-1, time=time)
        
                    
                    
                    
        #                output = {
        #                            'node': node,
        #                            'lambda': lamb,
        #                            'beta': beta,
        #                            'mu': mu,
        #                            'pDetection': probabilityDetection,
        #                            'delay': delay,
        #                            'duration': endingSimulation - startingSimulation
        #                        }
        #                
        #                out_file.write(json.dumps(output))
        #                out_file.write(',')
        
        
        
                    row = node + ',' + str(epsilon) + ',' + str(lamb) + ',' + str(beta) + ',' + str(mu) + ','
                            
                    for key, item in probabilityDetection.iteritems():
                        for pdepth in item:    
                            row = row + str(pdepth) + ','
                            
                    for key, item in delay.iteritems():
                        for deldepth in item:
                            row = row + str(deldepth) + ','
                            
                    row = row + str(endingSimulation-startingSimulation) + '\n'
                    
                    out_file.write(row)
                
##### DELAYS ###
#delays = np.zeros(shape=(5,3))
##delays[:] = np.inf
#counters = np.zeros(shape=(5,3))
#
#for key, value in resultSimulation.iteritems():
#    
#    for k in range(1, 6):
#        
#        for depth in range(3):
#            
#            if (value['delay'][k][depth] != np.inf):
#                
##                if value['delay'][k][depth] < delays[k-1][depth]:
##                    delays[k-1][depth] = value['delay'][k][depth]
#
#                delays[k-1][depth] += value['delay'][k][depth]
#                counters[k-1][depth] += 1
#            
#resultsDividedDelay = np.divide(delays, counters)         
#
#### p detection ###
#pDetections = np.zeros(shape=(5,3))
#countersDetections = np.zeros(shape=(5,3))
#
#for key, value in resultSimulation.iteritems():
#    
#    for k in range(1, 6):
#        
#        for depth in range(3):
#            
#            if (value['pDetection'][k][depth] != -1):
#            
#                pDetections[k-1][depth] += value['pDetection'][k][depth]
#                countersDetections[k-1][depth] += 1
#            
#resultsDividedpDetection = np.divide(pDetections, countersDetections)   

if __name__ == '__main__':
    
    for node in nodeSimulationList:
        
        p = Process(target=worker, args=(node,))
        p.start()
#        p.join()

