#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:48:21 2017

@author: anr.putina
"""

class Point():
    
    def __init__(self, value, timestamp):
        self.covered = False
        self.value = value
        self.timestamp = timestamp
    
    def getCovered(self):
        return self.covered
    
    def getValue(self):
        return self.value
    
    def setTimestamp(self, timestamp):
        self.timestamp = timestamp