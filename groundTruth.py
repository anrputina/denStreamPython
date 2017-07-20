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
            'startTime': 1498755722500000000,
            'startIndex': 366,
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
            'startTime': 1498756044535000000,
            'startIndex': 438,
            'endTime': 1498756199112000000,
            'endIndex': 477,
            'node': 'spine3',
            'type': 'multiple'
        }
        self.addEvent(eventRecord)

    def simulationBGP_CLEAR2(self):
        eventRecord = {
            'name': 'event1',
            'startTime': 1498754400000,
            'endTime': 1498754520000,
            'node': 'leaf1',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event2',
            'startTime': 1498754640000,
            'endTime': 1498754760000,
            'node': 'spine4',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event3',
            'startTime': 1498754880000,
            'endTime': 1498755000000,
            'node': 'leaf8',
            'type': 'single'

        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event4',
            'startTime': 1498755120000,
            'endTime': 1498755300000,
            'node': 'spine2',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event5',
            'startTime': 1498755420000,
            'endTime': 1498755600000,
            'node': 'leaf2',
            'type': 'single'

        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event5',
            'startTime': 1498755420000,
            'endTime': 1498755600000,
            'node': 'leaf6',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event6',
            'startTime': 1498755720000,
            'endTime': 1498755900000,
            'node': 'spine1',
            'type': 'single'
        }

        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event6',
            'startTime': 1498755720000,
            'endTime': 1498755900000,
            'node': 'spine3',
            'type': 'multiple'
        }

        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event7',
            'startTime': 1498756020000,
            'endTime': 1498756200000,
            'node': 'spine1',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event7',
            'startTime': 1498756020000,
            'endTime': 1498756200000,
            'node': 'spine2',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)
        
        eventRecord = {
            'name': 'event7',
            'startTime': 1498756020000,
            'endTime': 1498756200000,
            'node': 'spine3',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)
        
        
    def simulationBGP_CLEAR3(self):
        
        ##indexStart : 76
        eventRecord = {
            'name': 'event1',
            'startTime': 1498754415519,
            'endTime': 1498754520000,
            'node': 'leaf1',
            'type': 'single'
        }
        
        self.addEvent(eventRecord)
        
        ### indexStart : 129
        eventRecord = {
            'name': 'event2',
            'startTime': 1498754656637,
            'endTime': 1498754760000,
            'node': 'spine4',
            'type': 'single'
        }
        self.addEvent(eventRecord)
        
        ### indexStart : 183
        eventRecord = {
            'name': 'event3',
            'startTime': 1498754885121,
            'endTime': 1498755000000,
            'node': 'leaf8',
            'type': 'single'

        }
        self.addEvent(eventRecord)
        
        ### indexStart : 232
        eventRecord = {
            'name': 'event4',
            'startTime': 1498755124567,
            'endTime': 1498755300000,
            'node': 'spine2',
            'type': 'single'
        }
        self.addEvent(eventRecord)
        
        ### indexStart : 303 
        eventRecord = {
            'name': 'event5leaf2',
            'startTime': 1498755424540,
            'endTime': 1498755600000,
            'node': 'leaf2',
            'type': 'single'

        }
        self.addEvent(eventRecord)
        
        ### indexStart : 304
        eventRecord = {
            'name': 'event5leaf6',
            'startTime': 1498755429032,
            'endTime': 1498755600000,
            'node': 'leaf6',
            'type': 'multiple'
        }
        self.addEvent(eventRecord)
        
        ### indexStart : 366
        eventRecord = {
            'name': 'event6spine1',
            'startTime': 1498755727878,
            'endTime': 1498755900000,
            'node': 'spine1',
            'type': 'single'
        }
        self.addEvent(eventRecord)
        
        ### indexStart : 368
        eventRecord = {
            'name': 'event6spine3',
            'startTime': 1498755731460,
            'endTime': 1498755900000,
            'node': 'spine3',
            'type': 'multiple'
        }
        self.addEvent(eventRecord)

        ### indexStart : 437        
        eventRecord = {
            'name': 'event7spine1',
            'startTime': 1498756050743,
            'endTime': 1498756200000,
            'node': 'spine1',
            'type': 'single'
        }
        self.addEvent(eventRecord)
        
        ### indexStart : 437
        eventRecord = {
            'name': 'event7spine2',
            'startTime': 1498756050202,
            'endTime': 1498756200000,
            'node': 'spine2',
            'type': 'multiple'
        }
        self.addEvent(eventRecord)
        
        ### indexStart : 439
        eventRecord = {
            'name': 'event7spine3',
            'startTime': 1498756048827,
            'endTime': 1498756200000,
            'node': 'spine3',
            'type': 'multiple'
        }
        
        self.addEvent(eventRecord)