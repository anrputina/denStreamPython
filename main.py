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

from visualization import Visualization

import matplotlib.pyplot as plt
from microCluster import MicroCluster
from sklearn.neighbors import NearestNeighbors

def normalize_matrix(df):
    return (df - df.mean())/df.std()


### PREPARE DATA
#df = pd.read_csv('leaf1_5min.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf1_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf2clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('spine4_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf8_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
df = pd.read_csv('spine2_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('dr01_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('dr01_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('spine3_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)



time = df['time']

#epoch = df['epoch']
df = df.drop(['time'], axis=1)
df = df[:500]

dfNormalized = normalize_matrix(df).dropna(axis=1)
#dfNormalized = df

bufferDf = dfNormalized[10:60]
testDf = dfNormalized[60:]


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
    den.runOnNewPoint(Point(sample.values))
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
        
features = ['paths-count', '0/RP0/CPU0free-application-memory', 'vrf__update-messages-received']
        
visual.plotOutliers(features, df, outliers, merged, truth, 59)


### label ###
time = time[:500]
result = time< 1
for event in truth.events:
    
    check = (time >= event['startTime']) & (time <= event['endTime'])

    result = result | check

df['label'] = result

### outputs ###
output = [False] * 60
result = den.history
for  event in result:
    
    if event['event'] == 'Outlier':
        output.append(True)
    if event['event'] == 'Merged':
        output.append(False)

df['result'] = output

tp = (df['label'] == True) & (df['result'] == True)
tn = (df['label'] == False) & (df['result'] == False)

fp = (df['label'] == False) & (df['result'] == True)
fn = (df['label'] == True) & (df['result'] == False)

precision = tp.sum() / float((tp.sum() + fp.sum()))
recall = tp.sum() / float((tp.sum() + fn.sum()))