# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 11:43:53 2018

@author: abdullahbabgi
"""

from sklearn.cluster import AffinityPropagation

import geojson
import geoql
import geoleaflet
import requests
import urllib.request
import json
import datetime
import uuid 
import numpy
from sklearn import metrics
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

pi=numpy.pi
tan=numpy.tan
log=numpy.log

z=[x[1:3] for x in zipcodes[2215]]
y=[x[1:3] for x in zipcodes[2215]]






mapWidth = 20000
mapHeight = 10000

x=[0]*len(z)
y=[0]*len(z)
distance=[0]*len(z)

for i in range(len(z)):
    latitude= float(z[i][1])
    longitude= float(z[i][0])
    

    x[i]= (longitude+180)*(mapWidth/360)
    
    latRad = latitude*pi/180

    mercN = log(tan((pi/4)+(latRad/2)))
    y[i]     = (mapHeight/2)-(mapWidth*mercN/(2*pi))
    
    


plt.plot(x, y, 'ro')
plt.show()
    
X=[0]*len(x)

for i in range(len(X)):
    X[i]=[x[i],y[i]]
    


######################
"""from sklearn.cluster import KMeans
    
kmeans = KMeans(n_clusters=8).fit(X)
labels=kmeans.labels_
"""

# Compute Affinity Propagation
af = AffinityPropagation(preference=(len(X)/20)).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_



################### PLOT ################### 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#m=('s', 'x', 'o', '^', 'v', '*', 'd')
colors = ('blue', 'lightgreen', 'gray', 'cyan', 'yellow', 'black','green')
cmap = ListedColormap(colors[:len(numpy.unique(y))])

plt.scatter(x, y,c=labels, cmap=plt.cm.Paired, edgecolors='k')  #marker=m    , edgecolors='k'
fig = plt.gcf()
############################################