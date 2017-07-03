#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 11:28:08 2017

@author: anr.putina
"""

import math
    
def distance(pointA, pointB):
    distance = 0.0
    
    for pos in range(len(pointA)):
        dist = pointA[pos]-pointB[pos]
        distance += dist*dist
    
    return math.sqrt(distance)    
    

class denDBScan():
    
    def __init__(self, epsilon, mu, microClusters, timestamp):
        self.epsilon = epsilon
        self.mu = mu
        self.microClusters = microClusters
        self.timestamp = timestamp
        self.clusters = []

    def run(self):
        
        for microCluster in self.microClusters:
            
            if not microCluster.covered:
                
                microCluster.covered = True
                neighborhood = self.getNeighborhood(microCluster)
                
                cluster = []
                cluster.append(microCluster)
                if len(neighborhood) > 0:
                    self.expandCluster(cluster, neighborhood)
                    
                    self.clusters.append(cluster)
                    
                    
    def expandCluster(self, cluster, neighborhood):
        
        for microCluster in neighborhood:
            
            if not microCluster.covered:
                microCluster.covered = True
                cluster.append(microCluster)
                
                newNeighborhood = self.getNeighborhood(microCluster)
                
                if len(newNeighborhood) > 0 :
                    
                    self.expandCluster(cluster, neighborhood)
                
                
    def getNeighborhood(self, microCluster):
        
        neighborhood = []
        
        for newCluster in self.microClusters:
            
            if not newCluster.covered:
                
                reachable = self.getReachability(microCluster, newCluster)
                
                if (reachable):
                    neighborhood.append(newCluster)
        
        return neighborhood
        
    def getReachability(self, microCluster, newCluster):
        
        # check weight
        
        if newCluster.weight >= self.mu:
                        
            # check distance
            
            dist = distance(pointA=microCluster.getCenter(self.timestamp), pointB=newCluster.getCenter(self.timestamp))
                        
            if dist <= 2 * self.epsilon:
                
                print 'qui'
                
                ### IMPLEMENT ALSO RADIUS ###
                
                return True
