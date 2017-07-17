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
            'name': 'event1',
            'startTime': 1498754415519000000,
            'startIndex': 76,
            'endTime': 1498754521434000000,
            'endIndex': 100,
            'node': 'leaf1',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event2',
            'startTime': 1498754656637000000,
            'startIndex': 129,
            'endTime': 1498754760063000000,
            'endIndex': 154,
            'node': 'spine4',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event3',
            'startTime': 1498754885121000000,
            'startIndex': 183,
            'endTime': 1498755000770000000,
            'endIndex': 208,
            'node': 'leaf8',
            'type': 'single'

        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event4',
            'startTime': 1498755124567000000,
            'startIndex': 232,
            'endTime': 1498755304432000000,
            'endIndex': 276,
            'node': 'spine2',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event5',
            'startTime': 1498755424734000000,
            'startIndex': 303,
            'endTime': 1498755601181000000,
            'endIndex': 343,
            'node': 'leaf2',
            'type': 'single'

        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event5',
            'startTime': 1498755419850000000,
            'startIndex': 304,
            'endTime': 1498755601181000000,
            'endIndex': 343,
            'node': 'leaf6',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event6',
            'startTime': 1498755721694000000,
            'startIndex': 366,
            'endTime': 1498755900264000000,
            'endIndex': 410,
            'node': 'spine1',
            'type': 'single'
        }

        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event6',
            'startTime': 1498755731460000000,
            'startIndex': 368,
            'endTime': 1498755900264000000,
            'endIndex': 410,
            'node': 'spine3',
            'type': 'multiple'
        }

        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event7',
            'startTime': 1498756020858000000,
            'startIndex': 437,
            'endTime': 1498756199112000000,
            'endIndex': 477,
            'node': 'spine1',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event7',
            'startTime': 1498756020858000000,
            'startIndex': 438,
            'endTime': 1498756199112000000,
            'endIndex': 477,
            'node': 'spine2',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event7',
            'startTime': 1498756020858000000,
            'startIndex': 438,
            'endTime': 1498756199112000000,
            'endIndex': 477,
            'node': 'spine3',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)