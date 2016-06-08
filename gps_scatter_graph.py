#!/usr/bin/env python
import json
from bokeh.charts import Scatter, output_file,show
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.models import FixedTicker
import numpy as np

from bokeh.sampledata.autompg import autompg as df

#Get data from json file
with open("gps_sd.json") as definitions:
	json_data = json.load(definitions)

#Pull the status
gps_lat = [ element['gps_latitude'] for element in json_data]
gps_long = [ element['gps_longitude'] for element in json_data]

p = figure(title="GPS")
for i in gps_lat:
	for j in gps_long:
		p.scatter(i,j,marker='circle', line_color="#6666ee",fill_color="#ee6666", fill_alpha=1.0, size=8)

#def one_scatter(p,x,y,typestr):
#	p.scatter(x,y,marker=typestr, line_color="#6666ee",fill_color="#ee6666", fill_alpha=1.0, size=8)

#p = figure(title="GPS")

#for i in range(len(binary_array)):
#	for j in range(len(binary_array[i])):
#			one_scatter(p,i,j,"circle")

#df = zip(gps_lat,gps_long)
#df = np.vstack((gps_lat,gps_long)).T
#print df
#p = Scatter(df, x='mpg', y='hp', title="HP vs MPG",
#            xlabel="Miles Per Gallon", ylabel="Horsepower")
#ticks = range(0,32)
#p.yaxis[0].ticker=FixedTicker(ticks=ticks)
#p.xgrid.band_fill_alpha = 0.1
#p.xgrid.band_fill_color = 'navy"'
#print xyvalues
#scatter = Scatter(xyvalues,title="scatter", legend="top_left", ylabel="iterations")
# output to static HTML file
output_file("gps_scatter.html",title="GPS Lat Long")
show(p)
