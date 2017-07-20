#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:49:15 2017

@author: anr.putina
"""

import pandas as pd
import matplotlib.pyplot as plt
from visualization import Visualization

visual = Visualization()

node='spine3'
df = pd.read_csv(node+'_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df['time'] = df['time'] / 1000000000.
#node='leaf8'
#df2 = pd.read_csv(node+'_clearbgp.csv').dropna().drop('Unnamed: 0', axis=1)
#df2['time'] = df2['time'] / 1000000000.

#visual.plotHistTimeDifference([df,df2], bins=15)
#visual.plotTimes([df,df2])


#
## See ground truth from node itself
fig, ax = plt.subplots()

ax.plot(df['time'], df['paths-count'], marker='x')
position=368
ax.axvspan(df['time'].loc[position], df['time'].loc[position+50], alpha=0.5, color='red')



### check on leaf1 ###
#
#fig, ax = plt.subplots()
#
#ax.plot(df['time'], df['paths-count'], marker='x')
#checkvalue = 1498756044535000000
#ax.axvspan(checkvalue, checkvalue + 50000000000, alpha=0.5, color='red')
#
