#!/usr/bin/env python
import json
from bokeh.charts import Scatter, output_file,show
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.models import FixedTicker
import numpy as np
import pandas as pd

from bokeh.sampledata.autompg import autompg as df

#Get data from json file
with open("gps_sd.json") as definitions:
	json_data = json.load(definitions)


#Filter out 0,0
def filter_crap(pair):
	if not(pair[0]==0 and pair[1] == 0):
		return pair

def delta_e(p1,p2):
	return (p1[0]-p2[0],p1[1]-p2[1])

def deltas(coord_list):
	deltas = []
	#remove our first element
	p1 = coord_list.pop(0)
	save_head = p1
	for p2 in coord_list:
		deltas.append(delta_e(p1,p2))
		p1 = p2
	d.insert(0,save_head)
	return deltas

#Pull the status
gps_lat = [ float(element['gps_latitude']) for element in json_data]
gps_long = [ float(element['gps_longitude']) for element in json_data]

d = []
for i in range(len(gps_lat)):
	d.append((gps_lat[i],gps_long[i]))
d = filter(filter_crap,d)
gps_deltas = deltas(d)
delta_lats = [ delta_p[0] for delta_p in gps_deltas]
delta_longs =[ delta_p[1] for delta_p in gps_deltas]
d_lat = np.mean(delta_lats)
d_long = np.mean(delta_longs)

df = pd.DataFrame(d,columns=['lat','long'])
xlabel = u"Latitude \u0394Lat: "+"{:.10f}".format(d_lat)
ylabel = u"Longitude \u0394Long: "+"{:.10f}".format(d_long)
print df

p = Scatter(df, x='lat', y='long', title="GPS Lat and Long",
            xlabel=xlabel, ylabel=ylabel)

# output to static HTML file
output_file("gps_scatter.html",title="GPS Lat Long")
show(p)
