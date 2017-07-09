#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 10:14:24 2017

@author: anr.putina
"""

class groundTruth():
    
    def __init__(self):
        self.events = []
        pass
    
    def setEvents(self, events):
        pass
    
    def addEvent(self, event):
        self.events.append(event)
        
    def simulationBGP_CLEAR(self):
        eventRecord = {
            'startTime': 1498754403279000000,
            'startIndex': 73,
            'endTime': 1498754519173000000,
            'endIndex': 100
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'startTime': 1498754639663000000,
            'startIndex': 127,
            'endTime': 1498754760063000000,
            'endIndex': 154
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'startTime': 1498754880445000000,
            'startIndex': 181,
            'endTime': 1498755000770000000,
            'endIndex': 208
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'startTime': 1498755121008000000,
            'startIndex': 235,
            'endTime': 1498755304432000000,
            'endIndex': 276
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'startTime': 1498755419850000000,
            'startIndex': 302,
            'endTime': 1498755601181000,
            'endIndex': 343
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'startTime': 1498755721694000000,
            'startIndex': 370,
            'endTime': 1498755900264000000,
            'endIndex': 410
        }

        self.addEvent(eventRecord)
        
        eventRecord = {
            'startTime': 1498756020858000,
            'startIndex': 437,
            'endTime': 1498756199112000,
            'endIndex': 477
        }
        
        self.addEvent(eventRecord)