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
import pandas as pd

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
    
    def __init__(self, horizon=1000, epsilon=0.1, minPoints=4, beta=1, mu=1, initPointOption=2, startingPoints=[10,11]):
        self.horizon = horizon
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

        
        self.lamb = 0.1
        self.inizialized = False
        
        #For debug and performance evaluation
        #Count number of steps
        self.timestampStep = 0
                
    def resetLearningImpl(self):
        
#        self.currentTimestamp = datetime.datetime.now()

        if simulation:
            self.currentTimestamp = 0
        else:
            self.currentTimestamp = time.time()

        #self.lamb = -math.log(self.weightThreshold) / math.log(2) / float(self.horizon)
        self.inizialized = False
        
        self.pMicroCluster = Cluster()
        self.oMicroCluster = Cluster()
                
        self.tp = round(1/self.lamb * math.log((self.beta*self.mu)/(self.beta*self.mu-1)))+1
        
    def initialDBScan(self):
        
        for point in self.buffer:
            if not point.covered:
                point.covered=True
                neighborhood = self.getNeighbourhoodIDs(point)
                
                #print len(neighborhood)
                
                if (len(neighborhood) > self.minPoints):
                    mc = MicroCluster(point, self.currentTimestamp, self.lamb, self.currentTimestamp)
                    self.expandCluster(mc, neighborhood)
                    self.pMicroCluster.insert(mc)
            else:
                point.covered = False
                    
    def expandCluster(self, mc, neighborhood):
        
        for point in neighborhood:
            
            if not point.covered:
                point.covered = True
                mc.insert(point, self.currentTimestamp)
                newNeighborhood = self.getNeighbourhoodIDs(point)
                if (len(neighborhood) > self.minPoints):
                    self.expandCluster(mc, newNeighborhood)
            
    def getNeighbourhoodIDs(self, point):
        
        neighbourIDs = []
        
        for newPoint in self.buffer:
            if not newPoint.covered :
                dist = distance(point, newPoint)
                
                #print 'distance ' + str(point.value) + ' from ' + str(newPoint.value) + ' = ' + str(dist)
                
                if (dist<self.epsilon):
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
                minDist = distance(p, Point(cluster.getCenter(timestamp), self.currentTimestamp))
                
            dist = distance(p, Point(cluster.getCenter(timestamp), self.currentTimestamp))
#            print 'Distance p - cluster center: '+str(dist)
            dist -= cluster.getRadius(self.currentTimestamp)
            print 'Distance p - cluster: '+str(dist)

            if (dist < minDist):
                minDist = dist
                minCluster = cluster
                
        return minCluster
            
    
    def runOnNewPoint(self, point):
#        self.timestampStep += 1
#        self.currentTimestamp = datetime.datetime.now()
#        self.currentTimestamp = time.time()
        
        if simulation:
            self.currentTimestamp += 1
        else:
            self.currentTimestamp = time.time()

        ############
        ### INIT ###
        ############

        if not self.inizialized:
            self.buffer.append(point)
            if (len(self.buffer) >= self.initPointOption):
                self.resetLearningImpl()
                self.initialDBScan()
                self.inizialized = True
                
        #############
        ### MERGE ###
        #############
        
        else:
            merged = False
            
            if len(self.pMicroCluster.clusters) != 0:
                print ('in pMicroCluster')
                closestMicroCluster = self.nearestCluster(point, self.currentTimestamp, kind='cluster')
                
                print ('POS closest: ')+str(self.pMicroCluster.clusters.index(closestMicroCluster))
                
                backupClosestCluster = copy.copy(closestMicroCluster)
                backupClosestCluster.insert(point, self.currentTimestamp)
                              
                if (backupClosestCluster.getRadius(self.currentTimestamp) <= self.epsilon):
                    
                    closestMicroCluster.insert(point, self.currentTimestamp)
                    merged = True
                    self.pMicroCluster.show()
                    print 'MERGED'

            
            if not merged and len(self.oMicroCluster.clusters) != 0:
                
                print 'not merged and len oMicro'
                
                closestMicroCluster = self.nearestCluster(point, self.currentTimestamp, kind='outlier')
            
                backupClosestCluster = copy.copy(closestMicroCluster)
                backupClosestCluster.insert(point, self.currentTimestamp)
                
                if (backupClosestCluster.getRadius(self.currentTimestamp) <= self.epsilon):
                    closestMicroCluster.insert(point, self.currentTimestamp)
                    merged = True
                    
                    if (closestMicroCluster.weight > self.beta * self.mu):
                        self.oMicroCluster.clusters.pop(self.oMicroCluster.clusters.index(closestMicroCluster))
                        self.pMicroCluster.insert(closestMicroCluster)
                    
            if not merged:
                print 'not merged'
                newOutlierMicroCluster = MicroCluster(point, self.currentTimestamp, self.lamb, self.currentTimestamp)
                self.oMicroCluster.insert(newOutlierMicroCluster)
                    
            if self.currentTimestamp % self.tp == 0:
                
                print ('currentTime % tp')
                
                for cluster in self.pMicroCluster.clusters:
                    if cluster.weight < self.beta * self.mu:
                        self.pMicroCluster.clusters.pop(self.pMicroCluster.clusters.index(cluster))
                
                for cluster in self.oMicroCluster.clusters:

                    creationTimestamp = cluster.creationTimeStamp
                        
                    xs1 = math.pow(2, -self.lamb*(self.currentTimestamp - creationTimestamp + self.tp)) - 1
                    xs2 = math.pow(2, -self.lamb * self.tp) - 1
                    xsi = xs1 / xs2

                    if cluster.weight < xsi:
                        self.oMicroCluster.clusters.pop(self.oMicroCluster.clusters.index(cluster))
                
            
points=[]

step = 0
for x in [[1,1,1], [2,1,1], [3,1,1], [2,1,1], [1,1,1], [76,1,1], [77,1,1], [78,1,1], [79,1,1], [130,1,1], [131,1,1], [132,1,1], [133,1,1]]:
    p = Point(x, 0)
    step += 1
    points.append(p)
  
den = DenStream(horizon=150, epsilon=10, minPoints=2, beta=0.2, mu=10, initPointOption=2, startingPoints=points)


p = Point([2,1,1], 0)
den.runOnNewPoint(p)

p2 = Point([2,2,1], 1)
den.runOnNewPoint(p2)

p = Point([3,2,1], 2)
den.runOnNewPoint(p)
p = Point([75,1,1], 3)
den.runOnNewPoint(p)
p = Point([130,1,1], 4)
den.runOnNewPoint(p)



p = Point([7,1,1], 5)
den.runOnNewPoint(p)
#p = Point([8,1])
#den.runOnNewPoint(p)
#p = Point([9,1])
#den.runOnNewPoint(p)
#p = Point([10,1])
#den.runOnNewPoint(p)

#p = Point([13,1])
#den.runOnNewPoint(p)
#p = Point([14,1])
#den.runOnNewPoint(p)
#p = Point([15,1])
#den.runOnNewPoint(p)
#p = Point([16,1])
#den.runOnNewPoint(p)


#offlineScan = denDBScan(10, 1, den.pMicroCluster.clusters, den.currentTimestamp)
#offlineScan.run()

#p = Point([74,1])
#den.runOnNewPoint(p)
#p = Point([73,1])
#den.runOnNewPoint(p)
#p = Point([25,7])
#den.runOnNewPoint(p)
#
#p = Point([77,1000])
#den.runOnNewPoint(p)






















