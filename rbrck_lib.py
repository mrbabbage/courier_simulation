
"""
Created on Mon Mar  5 17:30:19 2018

@author: abdullahbabgi
"""





"""
gmaps = googlemaps.Client(key='AIzaSyCW6k0oDjxS-2gTR4XzZ3iX8SWioIeKZGk')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
print(list(geocode_result[0].values())[2].get('location'))


# Request directions via Driving
now = datetime.now()
directions_result = gmaps.directions((40.714224,-73.961452),
                                     (40.7290229,-73.9806781)
                                     ,waypoints=(40.7285676,-74.0059123)
                                     ,optimize_waypoints=True
                                     ,departure_time=now)

print(list(directions_result[0].values())[5][0].get('duration').get('value'))
"""

""" Reading in Boston Street Address Data from:
    https://data.boston.gov/dataset/live-street-address-management-sam-addresses"""







import folium
import geojson
import geoql
import requests
import json
import time
import csv 
import os
import googlemaps
from datetime import datetime
from operator import itemgetter
from geopy.distance import vincenty
from copy import deepcopy

""" base[0] [2215, -71.1036706046, 42.3464186693, 'Aberdeen St']"""
def reduce_address(zipcode):
    base=deepcopy(zipcode)
    result=[]
    while len(base)>0:
        base_d = deepcopy(base)
        result.append(base_d[0])
        base[0][0]=0
        for i in range(len(base)-2):
            #print(len(base))
            #print(base[0])
            #print(i+1)
            #print(base[i+1])
            a=base[0][1:3]
            b=base[i+1][1:3]
            distance=vincenty(a,b).miles
            if distance<=0.06 and base[i+1][0]!=0 and base[0][-1]==base[i+1][-1]:
                base[i+1][0]=0
        base=[x for x in base if x[0]!=0]
    return result

#filters all the unique entries and according to the acceptable zipcodes
def filter_all(full,acceptable):
    result=[]
    for x in full:
        if x not in result and x[0] in acceptable:
            result.append(x)
    return result

#filters according to 1 zipcode
def filter_zip(full,zipcode):
    result=[]
    for x in full:
        if x[0] ==zipcode:
            result.append(x)
    return result

#filters according to a list of acceptable zipcodes

def filter_list_of_zip(full_unique,acceptable):
    zipcodes={}
    for x in acceptable:
        for m in full_unique:
            if x in zipcodes and x==m[0] and m not in zipcodes[x]:
                zipcodes[x].append(m)
            elif x not in zipcodes:
                zipcodes[x]=[]
    return zipcodes



def plot_points(inputs):
    map = folium.Map(location=[42.3522147,-71.0696215], zoom_start=13)
    folium.TileLayer('cartodbpositron').add_to(map)
    for i in range(len(inputs)):
        lat=inputs[i][2]
        lon=inputs[i][1]
        folium.Marker([lat,lon],popup='',icon=folium.Icon(color='red',icon='')).add_to(map)
    map.save('rbrck_dropoffs_add.html')
    return
    
    
    
    