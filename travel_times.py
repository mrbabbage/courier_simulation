#!/usr/bin/env python

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAzlWRJShTKDbxXe1GFrlr7oFFlYmxjxbg')

def get_travel_time(src_lat=18.997739, src_lon=72.841280, dst_lat=18.880253, dst_lon=72.945137):
	now = datetime.now()
	directions_result = gmaps.directions("%f, %f" % (src_lat, src_lon),
	                                     "%f, %f" % (dst_lat, dst_lon),
	                                     mode="driving",
	                                     avoid="ferries",
	                                     departure_time=now
	                                    )

	mins = directions_result[0]['legs'][0]['duration']['value']
	return mins

if __name__ == '__main__':
	mins = get_travel_time()
	print(mins)