#!/usr/bin/env python
import json
from bokeh.charts import Scatter, output_file,show
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.models import FixedTicker


#Get data from json file
with open("gps_sd.json") as definitions:
	json_data = json.load(definitions)

#Pull the status
status = [ element['status'] for element in json_data]

#Convert to int then get the binary strings, da fuq is that list bin int, welcome to python
binary_array = [ list(bin(int(s))[2:].zfill(5)) for s in status]
print binary_array

def zero_scatter(p,x,y,typestr):
	p.scatter(x,y,marker=typestr, line_color="#6666ee",fill_color="#ee6666", fill_alpha=0.25, size=8)
def one_scatter(p,x,y,typestr):
	p.scatter(x,y,marker=typestr, line_color="#6666ee",fill_color="#ee6666", fill_alpha=1.0, size=8)

p = figure(title="scatter.py")

for i in range(len(binary_array)):
	for j in range(len(binary_array[i])):
		if binary_array[i][j] == '0':
			zero_scatter(p,i,j,"circle")
		else:
			one_scatter(p,i,j,"circle")

ticks = range(0,32)
p.yaxis[0].ticker=FixedTicker(ticks=ticks)
p.xgrid.band_fill_alpha = 0.1
p.xgrid.band_fill_color = 'navy"'
#print xyvalues
#scatter = Scatter(xyvalues,title="scatter", legend="top_left", ylabel="iterations")
# output to static HTML file
output_file("circles.html",title="circles.py test")
show(p)
