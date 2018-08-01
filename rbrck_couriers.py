# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 17:17:31 2018

@author: abdullahbabgi

This program is meant to simulate the pick up and delivery 
of packages in the boston and camrbidge area. 

The steps involved: 
1. Caulculate time for pick up from all stores. 
2. Randomize drop off locations to residential addresses in 
   the selected 18 zipcodes. 
3. Use the google maps api to calculate the time needed to
   visit x locations (x locations). 
4.  Iterate for x = [1,10000]
5. Visualize locations vs time & locations vs couriers
   as well as distance vs time & distance vs couriers

Assumptions: 
* 15 mins to arrange the packages for every store.
* Number of drop offs per zipcode are a function of the
  populace in that area.
* Courier shifts are 8 hours, thus 9 hour delivery times
  needs 2 couriers.
* Courier can walk 100m from one stop, so addresses near there are walked to.   

API's used: 
 

RBRCK only operates in the following zipcodes (boston sam data) are: 
[
[2215,26125],
[2116,20628],
[2114,11999],
[2111,7383],
[2113,6915],
[2108,3825],
[2109,3771],
[2210,2090],
[2110,1733],
]


                                     
"""

import rbrck_lib

###############################################
""" Format is [Zipcode, Longitude, Latitude, Street Address] """

#os.chdir(r'/Users/abdullahbabgi/Downloads')
lon=[]
lat=[]
streetname=[]
zipcode=[]
full=[]

with open('boston_addresses_c.csv') as f:
    f.readline()
    reader = csv.reader(f, delimiter=",")
    for i in reader:
        if i[4] == 'Boston':
            lon.append(float(i[0]))
            lat.append(float(i[1]))
            streetname.append(str(i[3]))
            zipcode.append(int(i[5]))
            full.append([int(i[5]),float(i[0]),float(i[1]),str(i[3])])

full=sorted(full, key=itemgetter(0))

###############################################
""" Filtering data by removing redundancies and including only RBRCK served zipcodes"""
acceptable=[2215,2116,2108,2114,2113,2109,2110,2210,2111]
full_unique=reduce_address(filter_all(full,acceptable))



""" Filtering data by RBRCK served zipcodes"""
zipcodes=filter_list_of_zip(full_unique,acceptable)


plot_points(zipcodes[2116])


# #############################################################################


