#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 16:41:44 2017

@author: anr.putina
"""

import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

import glob
df = pd.DataFrame(columns=['node',
     ' epsilon',
     ' lambda',
     ' beta',
     ' mu',
     ' pdetectk1d0',
     ' pdetectk1d1',
     ' pdetectk1d2',
     ' pdetectk2d0',
     ' pdetectk2d1',
     ' pdetectk2d2',
     ' pdetectk3d0',
     ' pdetectk3d1',
     ' pdetectk3d2',
     ' pdetectk4d0',
     ' pdetectk4d1',
     ' pdetectk4d2',
     ' pdetectk5d0',
     ' pdetectk5d1',
     ' pdetectk5d2',
     ' delayK1d0',
     ' delayK1d1',
     ' delayK1d2',
     ' delayK2d0',
     ' delayK2d1',
     ' delayK2d2',
     ' delayK3d0',
     ' delayK3d1',
     ' delayK3d2',
     ' delayK4d0',
     ' delayK4d1',
     ' delayK4d2',
     ' delayK5d0',
     ' delayK5d1',
     ' delayK5d2',
     ' duration'])



for result in glob.glob("*.csv"):
    
    d = pd.read_csv(result)
    df = pd.concat([df, d])
    

df2 = df[df[' pdetectk1d0'] > -1]

groups = df2.groupby([' epsilon',' lambda']).mean()



import matplotlib
matplotlib.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Y = list(groups.index.levels[0])
X = list(groups.index.levels[1])
X, Y = np.meshgrid(X, Y)

#feature = ' pdetectk3d0'
#a = np.array(groups[feature].values)
#a = a.reshape(9,8)
#ax.plot_surface(X, Y, a, color='black', linewidth=0, antialiased=False)
##
#feature = ' pdetectk3d1'
#a = np.array(groups[feature].values)
#a = a.reshape(9,8)
#ax.plot_surface(X, Y, a, color = 'r' , linewidth=0, antialiased=False)

feature = ' pdetectk3d2'
a = np.array(groups[feature].values)
a = a.reshape((8,9))
ax.plot_surface(X, Y, a, cmap=cm.coolwarm, linewidth=0, antialiased=False, label='parametric curve')
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_ylabel('epsilon')
ax.set_xlabel('lambda')
ax.set_zlabel('detection probability')

feature = ' pdetectk4d2'
a = np.array(groups[feature].values)
a = a.reshape((8,9))
ax.plot_surface(X, Y, a, color='black', linewidth=0, antialiased=False, label='parametric curve')
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_ylabel('epsilon')
ax.set_xlabel('lambda')
ax.set_zlabel('detection probability')

feature = ' pdetectk5d2'
a = np.array(groups[feature].values)
a = a.reshape((8,9))
ax.plot_surface(X, Y, a, color='red', label='parametric curve')
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_ylabel('epsilon')
ax.set_xlabel('lambda')
ax.set_zlabel('detection probability')

ax.legend()


#ax.set_zlim(-0, 1.01)
########## END PLOT!!! ####

## START NEW PLOT ###
#groups = df2.groupby([' epsilon',' mu']).mean()
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#
##x = groups.index[0][:]
#X = list(groups.index.levels[0])
#Y = list(groups.index.levels[1])
#X, Y = np.meshgrid(X, Y)
#
#feature = ' pdetectk3d0'
#a = np.array(groups[feature].values)
#a = a.reshape(8,8)
#ax.plot_surface(X, Y, a, color='black', linewidth=0, antialiased=False)
#
#feature = ' pdetectk3d1'
#a = np.array(groups[feature].values)
#a = a.reshape(8,8)
#ax.plot_surface(X, Y, a, color = 'r' , linewidth=0, antialiased=False)
#
#feature = ' pdetectk3d2'
#a = np.array(groups[feature].values)
#a = a.reshape(8,8)
#ax.plot_surface(X, Y, a, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#ax.set_xlabel('epsilon')
#ax.set_ylabel('mu')
#ax.set_zlabel('detection probability')










