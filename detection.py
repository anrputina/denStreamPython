#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:08:31 2017

@author: anr.putina
"""

import numpy as np

class detection():
    
    def __init__(self, name, depth):
        self.name = 'k='+str(name)
        self.depthTopology = depth
        self.detections = [0] * depth
        self.events = [0] * depth
        self.delays = [np.inf] * depth
        self.delaysMin = [np.inf] * depth
    
    def getDetections(self):
        return self.detections
    
    def getEvents(self):
        return self.events
    
    def addDetection(self, position):
        self.detections[position] += 1
        self.events[position] += 1
        
    def addEvents(self, position):
        self.events[position] += 1
        
    def addDelay(self, position, delay):
        if (self.delays[position] == np.inf):
            self.delays[position] = 0
        
        self.delays[position] += delay 
        
    def addDelayMin(self, position, delay):
        if delay < self.delaysMin[position]:
            self.delaysMin[position] = delay 
        else :
            pass
            
            
#    def getProbabilityDetection(self):
#        if (self.events != 0):
#            return float(self.detections)/float(self.events)
#        else:
#            return -1
        

    def getListProbabilityDetection(self):
        
        listProbability = []
        for depth in range(self.depthTopology):
            
            if (self.events[depth] != 0):
                listProbability.append(float(self.detections[depth])/float(self.events[depth]))
            else:
                listProbability.append(-1)
                
        return listProbability
            
    def getMeanDelay(self):
        
        listDelays = []
        
        for depth in range(self.depthTopology):
            
            if (self.events[depth] != 0):
                listDelays.append(np.divide(self.delays[depth], float(self.events[depth])))
            else:
                listDelays.append(self.delays[depth])
        
        return listDelays
                
    def getMinDelay(self):
        
        listDelays = []
        
        for depth in range(self.depthTopology):
            
            if (self.events[depth] != 0):
                listDelays.append(self.delaysMin[depth])
            else:
                listDelays.append(self.delaysMin[depth])
                
        return listDelays
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        