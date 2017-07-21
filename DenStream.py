#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:48:32 2017

@author: anr.putina
"""

simulation = True

import sys
import copy
import math
import time
import datetime
import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN

from point import Point
from cluster import Cluster
from microCluster import MicroCluster

from denDBScan import denDBScan

def distance(pointA, pointB):
    distance = 0.0
    
    for pos in range(len(pointA.value)):
        dist = pointA.value[pos]-pointB.value[pos]
        distance += dist*dist
    
    return math.sqrt(distance)
    
class DenStream():
    
    def __init__(self, lamb, epsilon=0.1, minPoints=4, beta=1, mu=1, initPointOption=2, startingPoints=[10,11]):
        self.epsilon = epsilon
        self.minPoints = minPoints
        self.beta = beta
        self.mu = mu
        self.initPointOption = initPointOption
        self.buffer = startingPoints
        self.weightThreshold = 0.01;
        
        ###############################
        ### TIME or TIMESTAMP       ###
        ### Simulation or real time ###
        ###############################
#        self.currentTimestamp = datetime.datetime.now()
        
        if simulation:
            self.currentTimestamp = 0
        else:
            self.currentTimestamp = time.time()

        
        self.lamb = lamb
        self.inizialized = False
        
        #For debug and performance evaluation
        #Count number of steps
        self.timestampStep = 0
        
        self.historyBool = False
        
    def setHistory(self, state):
        self.historyBool = state
        
        if state == True:
            self.history = []
        
    def resetLearningImpl(self):
        
        if simulation:
            self.currentTimestamp = 0
        else:
            self.currentTimestamp = time.time()

        self.inizialized = False
        
        self.pMicroCluster = Cluster()
        self.oMicroCluster = Cluster()
                
        self.tp = round(1/self.lamb * math.log((self.beta*self.mu)/(self.beta*self.mu-1)))+1
                
    def initialDBScan(self):
        
        print 'initialDBSCAN'
        
        for point in self.buffer:
            if not point.covered:
                point.covered=True
                neighborhood = self.getNeighbourhoodIDs(point)
                
                #print len(neighborhood)
                
                if (len(neighborhood) > self.minPoints):
                    mc = MicroCluster(point, self.currentTimestamp, self.lamb)
                    self.expandCluster(mc, neighborhood)
                    self.pMicroCluster.insert(mc)
            else:
                point.covered = False
             
    def initialDBScanSciLearn(self):
        
        db = DBSCAN(eps=8, min_samples=self.minPoints, algorithm='brute').fit(self.buffer)
        clusters = db.labels_
        self.buffer['clusters'] = clusters
        
        clusterNumber = np.unique(clusters)
        
        for clusterId in clusterNumber:
            
            if (clusterId != -1):
                
                cl = self.buffer[self.buffer['clusters'] == clusterId]
                cl = cl.drop('clusters', axis=1)
                
                sample = Point(cl.iloc[0].tolist())
                                
                mc = MicroCluster(sample, self.currentTimestamp, self.lamb)
                
                for sampleNumber in range(len(cl[1:])):
                    sample = Point(cl.iloc[sampleNumber].tolist())
                    mc.insertPoint(sample, self.currentTimestamp)
                    
                self.pMicroCluster.insert(mc)
                
    def initWithoutDBScan(self):
        
        sample = Point(self.buffer.iloc[0].tolist(), 0)
        
        mc = MicroCluster(sample, self.currentTimestamp, self.lamb)
        
        for sampleNumber in range(len(self.buffer[1:])):
            sample = Point(self.buffer.iloc[sampleNumber].tolist(), 0)
            mc.insertPoint(sample, self.currentTimestamp)
            
        self.pMicroCluster.insert(mc)
        
        self.epsilon = self.pMicroCluster.clusters[0].computeRadius(self.currentTimestamp) * 1.5

                
    def expandCluster(self, mc, neighborhood):
        
        for point in neighborhood:
            
            if not point.covered:
                point.covered = True
                mc.insertPoint(point, self.currentTimestamp)
                newNeighborhood = self.getNeighbourhoodIDs(point)
                if (len(neighborhood) > self.minPoints):
                    self.expandCluster(mc, newNeighborhood)
            
    def getNeighbourhoodIDs(self, point):
        
        neighbourIDs = []
        
        for newPoint in self.buffer:
            if not newPoint.covered :
                dist = distance(point, newPoint)
                #print 'distance ' + str(point.value) + ' from ' + str(newPoint.value) + ' = ' + str(dist)
                
#                print dist
                
                if (dist<self.epsilon):
#                    print 'ok'
                    neighbourIDs.append(newPoint)
        
        return neighbourIDs
        
    def nearestCluster (self, point, timestamp, kind):
        minDist = 0.0
        minCluster = None
        
        if kind == 'cluster':
            clusterList = self.pMicroCluster.clusters
        elif kind == 'outlier':
            clusterList = self.oMicroCluster.clusters
        else:
            sys.exit('Error in choosing kind nearestCluster type: if pMicroCluster or oMicroCluster')
        
        for cluster in clusterList:
            
            if (minCluster == None):
                minCluster = cluster
#                minDist = distance(point, Point(cluster.computeCenter(timestamp)))
                minDist = distance(point, Point(cluster.center, 0))
                
#            dist = distance(point, Point(cluster.computeCenter(timestamp)))
            dist = distance(point, Point(cluster.center, 0))

#            dist -= cluster.computeRadius(self.currentTimestamp)
            dist -= cluster.radius


            if (dist < minDist):
                minDist = dist
                minCluster = cluster
                
        return minCluster
            
    def runInitialization(self):
        self.resetLearningImpl()
#        self.initialDBScanSciLearn()
        self.initWithoutDBScan()
        self.inizialized = True
    
    def runOnNewPoint(self, point):
#        self.timestampStep += 1
#        self.currentTimestamp = datetime.datetime.now()
#        self.currentTimestamp = time.time()

        if simulation:
            self.currentTimestamp += 1
            point.setTimestamp(self.currentTimestamp)
        else:
            self.currentTimestamp = time.time()

        ############
        ### INIT ###
        ############

        if not self.inizialized:
            self.buffer.append(point)
            if (len(self.buffer) >= self.initPointOption):
                self.resetLearningImpl()
#                self.initialDBScan()
                self.initialDBScanSciLearn()
                self.inizialized = True
                
        #############
        ### MERGE ###
        #############
        
        else:
            merged = False
            
            if len(self.pMicroCluster.clusters) != 0:
#                print ('in pMicroCluster')
                closestMicroCluster = self.nearestCluster(point, self.currentTimestamp, kind='cluster')
                                
                backupClosestCluster = copy.deepcopy(closestMicroCluster)
                backupClosestCluster.insertPoint(point, self.currentTimestamp)
                
#                if (backupClosestCluster.computeRadius(self.currentTimestamp) <= self.epsilon):
                if (backupClosestCluster.radius <= self.epsilon):

                    
                    closestMicroCluster.insertPoint(point, self.currentTimestamp)

                    merged = True
                
                    if self.historyBool:
                        
                        record = {
                                    'event': 'Merged',
                                    'time': self.currentTimestamp,
                                    'cluster': closestMicroCluster,
                                    'realTime': point.realTimestamp
                                }
                        
                        self.history.append(record)
                    
#                    self.pMicroCluster.show()
#                    print 'MERGED'

            
            if not merged and len(self.oMicroCluster.clusters) != 0:
                
#                print 'not merged and len oMicro'

                closestMicroCluster = self.nearestCluster(point, self.currentTimestamp, kind='outlier')
            
                backupClosestCluster = copy.deepcopy(closestMicroCluster)
                backupClosestCluster.insertPoint(point, self.currentTimestamp)
                
#                if (backupClosestCluster.computeRadius(self.currentTimestamp) <= self.epsilon):
                if (backupClosestCluster.radius <= self.epsilon):

                    closestMicroCluster.insertPoint(point, self.currentTimestamp)
                    
                    if self.historyBool:
                    
                        record = {
                                    'event': 'Outlier',
                                    'time': self.currentTimestamp,
                                    'realTime': point.realTimestamp
                                }
                        
                        self.history.append(record)
                    
                    merged = True
                    
                    if (closestMicroCluster.weight > self.beta * self.mu):
                        self.oMicroCluster.clusters.pop(self.oMicroCluster.clusters.index(closestMicroCluster))
                        self.pMicroCluster.insert(closestMicroCluster)
                        
                    
            if not merged:
#                print 'not merged'
                newOutlierMicroCluster = MicroCluster(point, self.currentTimestamp, self.lamb)
                self.oMicroCluster.insert(newOutlierMicroCluster)
                
                if self.historyBool:
                    
                    record = {
                                'event': 'Outlier',
                                'time': self.currentTimestamp,
                                'realTime': point.realTimestamp
                            }
                    
                    self.history.append(record)
                    
            if self.currentTimestamp % self.tp == 0:
                                
                for cluster in self.pMicroCluster.clusters:
                    
                    cluster.updateParameters(self.currentTimestamp)
                    
                    if cluster.weight < self.beta * self.mu:
                        self.pMicroCluster.clusters.pop(self.pMicroCluster.clusters.index(cluster))
                        
                        if self.historyBool:
                            
                            record = {
                                        'event': 'pRemoved',
                                        'time': self.currentTimestamp,
                                        'cluster': cluster,
                                        'realTime': point.realTimestamp
                                    }
                            
                            self.history.append(record)
                        
                
                for cluster in self.oMicroCluster.clusters:

                    cluster.updateParameters(self.currentTimestamp)

#                    print 'cercare dentro outlier'
                    
                    creationTimestamp = cluster.creationTimeStamp
                        
                    xs1 = math.pow(2, -self.lamb*(self.currentTimestamp - creationTimestamp + self.tp)) - 1
                    xs2 = math.pow(2, -self.lamb * self.tp) - 1
                    xsi = xs1 / xs2

                    if cluster.weight < xsi:
                        
                        self.oMicroCluster.clusters.pop(self.oMicroCluster.clusters.index(cluster))
                        
                        if self.historyBool:
                            
                            record = {
                                        'event': 'oRemoved',
                                        'time': self.currentTimestamp,
                                        'cluster': cluster,
                                        'realTime': point.realTimestamp
                                    }
                            
                            self.history.append(record)