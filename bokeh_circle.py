#!/usr/bin/env python
import json
from bokeh.charts import Scatter, output_file,show
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.models import FixedTicker


#Get data from json file
with open("gps_sd.json") as definitions:
	json_data = json.load(definitions)

#64 bits
string_64 = "00100100110011011100011101101110 00111011100011000100001111011101 11011011011110000001001111111100 10010111100111011111100001011101 11001110100100110011010000100010 01100100111000001010111110110010 00100101111101101101100101000101 11110010010000110110111110101110 11000000000111110000000000111110 11000011000111011111100011101011 10001100000001101011000010101011 10000101110010111111011010000101 10111010001100100000010001111011 10111110100111000010100101110001 01001110110100110101001001001100 11001001010010011001001100111000 00100100110011011100011101101110 00111011100011000100001111011101 11011011011110000001001111111100 10010111100111011111100001011101 11001110100100110011010000100010 01100100111000001010111110110010 00100101111101101101100101000101 11110010010000110110111110101110 11000000000111110000000000111110 11000011000111011111100011101011 10001100000001101011000010101011 10000101110010111111011010000101 10111010001100100000010001111011 10111110100111000010100101110001 01001110110100110101001001001100 11001001010010011001001100111000"

#Split into bytes
bytes_array = string_64.split(' ')
#Split each string into an array
bit64_array = []
for b in bytes_array:
	bit64_array.append(list(b))


bitvalues_2d = [
			 [0,1,0,0],
			 [1,0,1,0],
			 [1,0,1,1],
			 [0,1,0,1],
			 [0,0,1,1],
			 [1,0,0,0],
			 [1,1,1,0],
			 [0,1,0,1],
			 [1,0,1,0],
			 [1,0,0,1],
			 [0,0,1,0],
			 [1,0,1,0],
			 [1,1,0,1],
			 [0,1,0,1],
			 [0,0,1,0],
			 [0,1,0,0],
			 [1,0,0,1]
			 ]

bitvalues_2d = bit64_array

# prepare some data, 16 total rows
xyvalues = OrderedDict()
xyvalues['one'] = []
xyvalues['zero'] = []


def zero_scatter(p,x,y,typestr):
	p.scatter(x,y,marker=typestr, line_color="#6666ee",fill_color="#ee6666", fill_alpha=0.25, size=16)
def one_scatter(p,x,y,typestr):
	p.scatter(x,y,marker=typestr, line_color="#6666ee",fill_color="#ee6666", fill_alpha=1.0, size=16)

#Traverse the matrix
for i in range(len(bitvalues_2d)):
	for j in range(len(bitvalues_2d[i])):
		if bitvalues_2d[i][j] == 0:
			xyvalues["zero"].append((i,j))
		else:
			xyvalues["one"].append((i,j))

p = figure(title="scatter.py")

for i in range(len(bitvalues_2d)):
	for j in range(len(bitvalues_2d[i])):
		if bitvalues_2d[i][j] == '0':
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
