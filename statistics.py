#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:06:54 2017

@author: anr.putina
"""

import copy
import numpy as np
from detection import detection

def findDistance(node, eventNode):
    
    if node == eventNode:
        return 0
    
    elif (('leaf' in node) and ('spine' in eventNode)) or (('spine' in node) and ('leaf' in eventNode)):
        return 1
    
    elif (('leaf' in node) and ('dr' in eventNode) or ('dr' in node) and ('leaf' in eventNode)):
        return 1
    
    elif ('dr' in node) and ('dr' in eventNode):
        return 1

    elif (('dr' in node) and ('spine' in eventNode) or ('spine' in node) and ('dr' in eventNode)):
        return 2
    
    elif ('leaf' in node) and ('leaf' in eventNode):
        return 2
    
    elif (('spine' in node) and ('spine' in eventNode)):
        return 2
    else:
        return 2

class statistics():
    
    def __init__(self, node):
        self.node = node
    
    def findMinDelay(self, df, truth):
        
        records = []
        
        for event in truth.events:
            
            for eventNode in event['node']:
                
                record = {}
                record['event'] = node+event['name']

                if node == eventNode:
                    record['hops'] = 0

                elif 'spine' in eventNode:
                    
                    record['hops'] = 1
                    
                else:
                    record['hops'] = 2
                    
            
                currentEvent = df[df['labels']==event['name']]
                indexes = currentEvent[currentEvent['result']==True].index
                                
                for i in range(5):
                    
                    if len(indexes) > i:
                        
                        record['detection'+str(i)] = True
                        record['delay'+str(i)] = indexes[i] - event['startIndex']
                    
                    else:
                        record['detection'+str(i)] = False
                        record['delay'+str(i)] = np.inf                     
    
                            
                records.append(record)
            
        return records
             

    def findProbabilityDetection(self, df, truth, time):
                

        depthTopology = 3
        result = {}
        
        for k in range(1, 6):
        
            pDetection = detection(k, depthTopology)
                    
            for event in truth.events:
                
                check = (time >= event['startTime']) & (time <= event['endTime'])
                currentEvent = df[check]
                
                indexes = currentEvent[currentEvent['result']==True].index
    
                position = findDistance(self.node, event['node'])
                
                if len(indexes) > k -1:
                    pDetection.addDetection(position)
                else:
                    pDetection.addEvents(position)
    
#                if node == event['node']:
#                                    
#                    position = 0
#                    if len(indexes) > k - 1 :
#                        pDetection.addDetection(position)
#                    else:
#                        pDetection.addEvents(position)
#                    
#                elif 'spine' in event['node']:
#                    
#                    position = 1
#                    
#                    if len(indexes) > k - 1 : 
#                        pDetection.addDetection(position)
#                    else:
#                        pDetection.addEvents(position)    
#                    
#                else:
#                    
#                    position = 2
#                    if len(indexes) > k - 1 :
#                        pDetection.addDetection(position)
#                    else:
#                        pDetection.addEvents(position)
                    
            result[k] = pDetection.getListProbabilityDetection()

        return result                
            
    def findDelayDetection(self, df, truth, time):
        
        depthTopology = 3
        result = {}
        
        for k in range(1, 6):
            
            delayDetection = detection(k, depthTopology)
            
            for event in truth.events:
                
                    
                check = (time >= event['startTime']) & (time <= event['endTime'])
                                                
                currentEvent = df[check]
                indexes = currentEvent[currentEvent['result']==True].index
                times = time[indexes]
                
                position = findDistance(self.node, event['node'])
                                
                if len(indexes) > k-1:    
                    delayDetection.addDetection(position)
                    delayDetection.addDelay(position, times.iloc[k-1] - event['startTime'])
                    
#                    print '---' + str(k)
#                    print 'problem: '+event['node']
#                    print 'problem: '+event['name']
#                    print position
#                    print times.iloc[k-1] - event['startTime']
                    
                    if (times.iloc[k-1] - event['startTime'] < 0):
                        print 'HEREEEEE'
#                        print '---' + str(k)
#                        print 'problem: '+event['node']
#                        print 'problem: '+event['name']
#                        print position
#                        print times.iloc[k-1] - event['startTime']
                    
                    delayDetection.addDelayMin(position, times.iloc[k-1] - event['startTime'])

                else:
                    delayDetection.addEvents(position)
            
#            result[k] = delayDetection.getMeanDelay()
            result[k] = delayDetection.getMinDelay()

        return result
                
            
            
        
                