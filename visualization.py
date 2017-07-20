#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 10:35:07 2017

@author: anr.putina
"""

import matplotlib.pyplot as plt
import matplotlib.pylab as pl

class Visualization():
    
    def __init__(self):
        pass
    
    def plotOutliers(self, features, df, outliers, merged, truth, stepsTrain=10):
        
        plotNumber = 0
        fig, ax = plt.subplots(len(features), sharex=True)
#        ax[0].set_title('Nome Grafico')

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
                if event['type'] == 'single':
                    ax[plotNumber].axvspan(event['startIndex'], event['endIndex'], alpha=0.5, color='red')
            
            if 'free-application-memory' in feature:
                ax[plotNumber].set_ylabel('free memory')
            elif 'vrf__update-messages-received' in feature:
                ax[plotNumber].set_ylabel('update msg rx')
            else:
                ax[plotNumber].set_ylabel(feature)    
            plotNumber += 1

        ax[len(features)-1].set_xlabel('Simulation Step')
  
    def plotOutliersInteractive(self, features, df, outliers, merged, truth, stepsTrain=10):
        
        plotNumber = 0
        fig, ax = pl.subplots(len(features), sharex=True)
#        ax[0].set_title('Nome Grafico')

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
                if event['type'] == 'single':
                    ax[plotNumber].axvspan(event['startIndex'], event['endIndex'], alpha=0.5, color='red')
            
            if 'free-application-memory' in feature:
                ax[plotNumber].set_ylabel('free memory')
            elif 'vrf__update-messages-received' in feature:
                ax[plotNumber].set_ylabel('update msg rx')
            else:
                ax[plotNumber].set_ylabel(feature)    
            plotNumber += 1

        ax[len(features)-1].set_xlabel('Simulation Step')
     
    def plotOutliersInteractiveTimestamp(self, features, df, outliers, merged, truth, stepsTrain=10, time=0):
        
        plotNumber = 0
        fig, ax = pl.subplots(len(features), sharex=True)
#        ax[0].set_title('Nome Grafico')


        for feature in features:
            
            ax[plotNumber].plot(time, df[feature])
            
            for outlier in outliers:
                ax[plotNumber].plot(time.iloc[stepsTrain+outlier['time']],
                                    df[feature].iloc[stepsTrain+outlier['time']],
                                    marker='o',
                                    color='r')
                
            for mergePoint in merged:
                ax[plotNumber].plot(time.iloc[stepsTrain+mergePoint['time']],\
                                    df[feature].loc[stepsTrain+mergePoint['time']],\
                                    marker='x',\
                                    color='g')
                            
            for event in truth.events:
                if event['type'] == 'single':
                    ax[plotNumber].axvspan(event['startTime'], event['endTime'], alpha=0.5, color='red')
            
            if 'free-application-memory' in feature:
                ax[plotNumber].set_ylabel('free memory')
            elif 'vrf__update-messages-received' in feature:
                ax[plotNumber].set_ylabel('update msg rx')
            else:
                ax[plotNumber].set_ylabel(feature)    
            plotNumber += 1

        ax[len(features)-1].set_xlabel('Simulation Step')
        
#    def plotSingleOutlier(self, feature, df, outliers, mergeg, truth, stepsTrain=10):
#        
#        fig, ax = plt.subplots()
#        
#        ax.plot(df[feature].values)
#        
#        for outlier in outliers:
#            ax.plot(stepsTrain + outlier['time'],
#                    df[feature].iloc[stepsTrain+outlier['time']],
#                    marker='o',
#                    color='r')
#            
#        for mergePoint in merged:
#            ax[plotNumber].plot(stepsTrain+mergePoint,\
#                                df[feature].iloc[stepsTrain+mergePoint],\
#                                marker='x',\
#                                color='g')
#            
#        for event in truth.events:
#            ax[plotNumber].axvspan(event['startIndex'], event['endIndex'], alpha=0.5, color='red')
#            
#        
#            
#            

    def plotHistTimeDifference(self, dfs, cumulative=False, bins=15, normed=True, scale='linear'):
        
        if len(dfs) == 1:
            
            fig, ax = plt.subplots()
            ax.hist(dfs[0]['time'].diff().dropna())
            
        if len(dfs) > 1:
            
            fig, ax = plt.subplots()
            
            alphaChannel = 1
            label = 'leaf1'
            for df in dfs:
                ax.hist(df['time'].diff().dropna(), alpha=alphaChannel, bins=bins, normed=normed, cumulative=cumulative, label=label)
                alphaChannel = 0.5
                label='leaf8'
            
            ax.set_yscale(scale)
            
            ax.legend()
            
            ax.set_xlabel('sample rate [s]')
            ax.grid()
        
            
                        
    def plotTimes(self, dfs):
        
        fig, ax = plt.subplots()
        
        label = 'leaf1'
        for df in dfs:
            
            ax.plot(df['time'], label=label)
            label = 'leaf8'
            
            
        ax.set_xlabel('sample number')
        ax.set_ylabel('timestamp')
        ax.legend(loc=4)
        ax.grid()
            
            
            
            
            
            
            
            
            
            
            
            
            