#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:46:51 2017

@author: anr.putina
"""

import math
import numpy as np
import datetime
radiusFactor = 1.8

class MicroCluster():
    def __init__(self, point, creationTimeStamp, lamb):
        self.points = []
        
        self.dimensions = len(point.value)
                
        self.creationTimeStamp = creationTimeStamp
        self.lastEditTimeStamp = self.creationTimeStamp
        self.lamb = lamb
        self.currentTimeStamp = creationTimeStamp
        
        self.N = 0
        self.weight = 0
        
        self.LS = [0] * self.dimensions
        self.SS = [0] * self.dimensions


#        ### V1 without real weight ### 
#        self.insert(point, currentTimeStamp)

        ### V2 with real weight ###
        self.insertPoint(point, creationTimeStamp)

        self.covered = False
        

#    def insert(self, point, timestamp):
#        self.N += 1
#        self.weight += 1
##        self.lastEditTimeStamp = datetime.datetime.now()
#        self.lastEditTimeStamp = timestamp
#        
#        self.points.append(point)
#        
#        for pos in range(len(point.value)):
#            self.LS[pos] += point.value[pos]
#            self.SS[pos] += point.value[pos] * point.value[pos]
            
    def insertPoint(self, point, timestamp):
        self.N += 1
        self.lastEditTimeStamp = timestamp
        self.points.append(point)
        
        self.weight = self.computeWeight(timestamp)
    
#    ### V1 without real weight ###         
#    def getCenter(self, timestamp):
#        
#        dt = timestamp - self.lastEditTimeStamp
#                
#        res = [0] * len(self.LS)
#        
#        for pos in range(len(self.LS)):
#            
#            res[pos] = self.LS[pos]
#            res[pos] *= math.pow(2, -self.lamb * dt)
#            res[pos] /= self.weight
#            
#        return res
    
#    ### V1 without real weight ###
#    def getRadius(self, timestamp):
#        
#        dt = timestamp - self.lastEditTimeStamp
#        
##        ### V1 ###
##        
##        cf1 = self.getCF1(dt)
##        cf2 = self.getCF2(dt)
##        
##        maxRad = 0
##        sumRad = 0
##        
##        for pos in range(len(self.LS)):
##            x1 = cf2[pos] / self.weight
##            x2 = math.pow(cf1[pos] / self.weight, 2)
##            
##            sumRad += (x1-x2)
##            
##            if (math.sqrt(x1-x2) > maxRad):
##                maxRad = math.sqrt(x1-x2)
#        
#
#        ### V2 ###
#        cf1 = self.getCF1(dt)
#        cf2 = self.getCF2(dt)
#        
#        maxRad = 0
#        sumRad = 0
#        
#        for pos in range(len(self.LS)):
#            
#            try:
#                rad = math.sqrt(np.linalg.norm(cf2[pos])/self.weight - np.power(np.linalg.norm(cf1[pos])/self.weight, 2))
#                
#                if (rad > maxRad):
#                    maxRad = rad
#            except: 
#                pass
#                print 'Negative value in sqrt!'
#                
#        return maxRad * radiusFactor
        
    def computeWeight(self, timestamp):
        
        newWeight = 0
        
        for point in self.points:
            
            newWeight += math.pow(2, -self.lamb * (timestamp - point.timestamp))
            
        return newWeight
            
        
    def computeCF1(self, timestamp):
        
        cf1 = [0] * len(self.LS)

        for point in self.points:
            
            for pos in range(len(self.LS)):    
                cf1[pos] += math.pow(2, -self.lamb * (timestamp - point.timestamp)) * point.value[pos]
        
        return cf1
    
    def computeCF2(self, timestamp):
        
        cf2 = [0] * len(self.SS)
        
        for point in self.points:
            
            for pos in range(len(self.LS)):
                
                cf2[pos] += math.pow(2, -self.lamb * (timestamp - point.timestamp)) * point.value[pos] * point.value[pos]
                
        return cf2
                
    def computeCenter(self, timestamp):
        
        cf1 = np.array(self.computeCF1(timestamp))
        w = self.computeWeight(timestamp)
        
        c = cf1 / w
        
        return c
            
    def computeRadius(self, timestamp):
        
        cf1 = np.array(self.computeCF1(timestamp))
        cf2 = np.array(self.computeCF2(timestamp))
        w = self.computeWeight(timestamp)
        
        maxRad = 0
                
        for pos in range(len(self.LS)):
            
            try:
                rad = math.sqrt((cf2[pos]/w) - (math.pow(cf1[pos]/w, 2)))
    
                if (rad > maxRad):
                    maxRad = rad
            except:
                pass
                    
        return maxRad * radiusFactor

    
#    ### V1 without real weight ###
#    def getCF1(self, dt):
#        cf1 = [0] * len(self.LS)
#        
#        for pos in range(len(self.LS)):
#            cf1[pos] = math.pow(2, -self.lamb * dt) * self.LS[pos]
#        
#        return cf1
#    
#    def getCF2(self, dt):
#        cf2 = [0] * len(self.SS)
#        
#        for pos in range(len(self.SS)):
#            cf2[pos] = math.pow(2, -self.lamb * dt) * self.SS[pos]
#            
#        return cf2