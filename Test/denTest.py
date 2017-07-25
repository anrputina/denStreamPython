#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:39:23 2017

@author: anr.putina
"""
import time as tm
import pandas as pd
import sys
sys.path.append('/Users/anr.putina/Desktop/denStreamPython')

from DenStream import DenStream
from point import Point
from microCluster import MicroCluster


def normalize_matrix(df):
    return (df - df.mean())/df.std()

#node = 'leaf1'
df = pd.read_csv('/Users/anr.putina/Desktop/denStreamPython/spine4_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)

samplesConsidered = 500
sampleSkip = 60

df['time'] = df['time'] / 1000000

time = df['time']
time = time[:samplesConsidered]

df = df.drop(['time'], axis=1)
df = df[:samplesConsidered]

dfNormalized = normalize_matrix(df).dropna(axis=1)

bufferDf = dfNormalized[10:sampleSkip]
testDf = dfNormalized[sampleSkip:]

epsilon = 10
lamb = 0.2
minPoints = 50
beta = 0.2
mu = 10
#bufferDf = bufferDf[:1]
#
#startingSimulation = tm.time()
#den = DenStream(epsilon=epsilon, lamb=lamb, minPoints=5, beta=beta, mu=mu, initPointOption=2, startingPoints=bufferDf[:1])
#den.setHistory(True)
#den.runInitialization()
#
#for sampleNumber in range(1, 49):
#    sample = bufferDf.iloc[sampleNumber]
#    den.runOnNewPoint(Point(sample.values, time.iloc[sampleNumber]))
#    tm.sleep(0.1)
#endingSimulation = tm.time()


microTest = MicroCluster(Point(bufferDf.iloc[0].tolist(), 0), 1, lamb)

for timesimulation in range(1, 50):
    point = Point(bufferDf.iloc[timesimulation].tolist(), timesimulation)
    point.setTimestamp(timesimulation)
    microTest.insertPoint(point, timesimulation)

print microTest.computeWeight(50)
print microTest.computeRadius(50)
print microTest.computeCenter(50)