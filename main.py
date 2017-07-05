#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:04:57 2017

@author: anr.putina
"""

import pandas as pd
from point import Point
from DenStream import DenStream
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
#df = pd.read_csv('spine2_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('dr01_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df = pd.read_csv('leaf6_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
df = pd.read_csv('spine3_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)



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
for sampleNumber in range(len(testDf)):
#for sampleNumber in range(1,8):
    sample = testDf.iloc[sampleNumber]
    den.runOnNewPoint(Point(sample.values))
    


#result = den.history
#outliers = []
#for event in result:
#    
#    if event['event'] == 'Outlier':
#        outliers.append(event)
#        
#fig, ax = plt.subplots()
#ax.plot(df['paths-count'].values)
#
#for outlier in outliers:
#    ax.plot(60+outlier['time'], df['paths-count'].iloc[60+outlier['time']], marker='o', color='r')
#
#

#### ground truth times ###

eventsGroundTruth = []

eventRecord = {
            'startTime': 1498754403279000000,
            'startIndex': 73,
            'endTime': 1498754519173000000,
            'endIndex': 100
        }

eventsGroundTruth.append(eventRecord)

eventRecord = {
            'startTime': 1498754639663000000,
            'startIndex': 127,
            'endTime': 1498754760063000000,
            'endIndex': 154
        }

eventsGroundTruth.append(eventRecord)

eventRecord = {
            'startTime': 1498754880445000000,
            'startIndex': 181,
            'endTime': 1498755000770000000,
            'endIndex': 208
        }

eventsGroundTruth.append(eventRecord)

eventRecord = {
            'startTime': 1498755121008000000,
            'startIndex': 235,
            'endTime': 1498755304432000000,
            'endIndex': 276
        }

eventsGroundTruth.append(eventRecord)

eventRecord = {
            'startTime': 1498755419850000000,
            'startIndex': 302,
            'endTime': 1498755601181000,
            'endIndex': 343
        }

eventsGroundTruth.append(eventRecord)

eventRecord = {
            'startTime': 1498755721694000000,
            'startIndex': 370,
            'endTime': 1498755900264000000,
            'endIndex': 410
        }

eventsGroundTruth.append(eventRecord)

eventRecord = {
            'startTime': 1498756020858000,
            'startIndex': 437,
            'endTime': 1498756199112000,
            'endIndex': 477
        }

eventsGroundTruth.append(eventRecord)

#############################


result = den.history
outliers = []
merged = []
for event in result:
    
    if event['event'] == 'Outlier':
        outliers.append(event)
        
    if event['event'] == 'Merged':
        merged.append(event['time'])
        
fig, ax = plt.subplots(2, sharex=True)

plot=0
feature = 'paths-count'
ax[plot].plot(df[feature].values)

stepsAfter = 59

for outlier in outliers:
    ax[plot].plot(stepsAfter+outlier['time'], df[feature].iloc[stepsAfter+outlier['time']], marker='o', color='r')

for mergePoint in merged:
    ax[plot].plot(stepsAfter+mergePoint, df[feature].iloc[stepsAfter+mergePoint], marker='x', color='g')

ax[plot].set_title('Leaf1 - clear BGP')
#ax[plot].set_xlabel('Simulation Step')
ax[plot].set_ylabel(feature)
#ax[plot].axis([0,40,1023, 1037])

for event in eventsGroundTruth:
    ax[plot].axvspan(event['startIndex'], event['endIndex'], alpha=0.5, color='red')


ax[plot].legend()

plot=1
feature = '0/RP0/CPU0free-application-memory'
ax[plot].plot(df[feature].values)

stepsAfter = 59

for outlier in outliers:
    ax[plot].plot(stepsAfter+outlier['time'], df[feature].iloc[stepsAfter+outlier['time']], marker='o', color='r')

for mergePoint in merged:
    ax[plot].plot(stepsAfter+mergePoint, df[feature].iloc[stepsAfter+mergePoint], marker='x', color='g')

ax[plot].set_title('Leaf1 - clear BGP')
ax[plot].set_xlabel('Simulation Step')
ax[plot].set_ylabel('free-application-memory')

for event in eventsGroundTruth:
    ax[plot].axvspan(event['startIndex'], event['endIndex'], alpha=0.5, color='red')




    
