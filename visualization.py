#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 10:35:07 2017

@author: anr.putina
"""

import matplotlib.pyplot as plt


class Visualization():
    
    def __init__(self):
        pass
    
    def plotOutliers(self, features, df, outliers, merged, truth, stepsTrain=10):
        
        plotNumber = 0
        fig, ax = plt.subplots(len(features), sharex=True)
        ax[0].set_title('Nome Grafico')

        for feature in features:
            
            ax[plotNumber].plot(df[feature].values)
            
            for outlier in outliers:
                ax[plotNumber].plot(stepsTrain+outlier['time'],
                                    df[feature].iloc[stepsTrain+outlier['time']],
                                    marker='o',
                                    color='r')
                
            for mergePoint in merged:
                ax[plotNumber].plot(stepsTrain+mergePoint,\
                                    df[feature].iloc[stepsTrain+mergePoint],\
                                    marker='x',\
                                    color='g')
                            
            for event in truth.events:
                ax[plotNumber].axvspan(event['startIndex'], event['endIndex'], alpha=0.5, color='red')
            
            if 'free-application-memory' in feature:
                ax[plotNumber].set_ylabel('free memory')
            elif 'vrf__update-messages-received' in feature:
                ax[plotNumber].set_ylabel('update msg rx')
            else:
                ax[plotNumber].set_ylabel(feature)    
            plotNumber += 1

        ax[len(features)-1].set_xlabel('Simulation Step')