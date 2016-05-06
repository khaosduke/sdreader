#!/usr/bin/env python
import json
from bokeh.plotting import *
#from bokeh.plotting import figure, output_file, show

#Get data from json file
with open("sd.json") as definitions:
	json_data = json.load(definitions)

# prepare some data
iterations = range(0,len(json_data)-1)
heading_degrees = []
heading_raw = []
pitch_deg = []
roll_deg = []

for element in json_data:
	heading_raw.append(element['heading_raw'])
	heading_degrees.append(element['heading_deg'])
	pitch_deg.append(element['pitch_deg'])
	roll_deg.append(element['roll_deg'])

# output to static HTML file
output_file("lines.html", title="line plot example")

# create a new plot with a title and axis labels
p = figure(title="Raw Heading", x_axis_label='iteration', y_axis_label='10th Degrees')
q = figure(title="Heading in Degrees", x_axis_label='iteration', y_axis_label='Degrees')
r = figure(title="Pitch in Degrees", x_axis_label='iteration', y_axis_label='Degrees')
s = figure(title="Roll in Degrees", x_axis_label='iteration', y_axis_label='Degrees')


# add a line renderer with legend and line thickness
p.line(iterations, heading_raw, legend="Heading Raw", line_width=2)
q.line(iterations, heading_degrees, legend="Heading degrees", line_width=2)
r.line(iterations, pitch_deg, legend="Pitch Degrees", line_width=2)
s.line(iterations, roll_deg, legend="Roll Degrees", line_width=2)

grid = gridplot([[p,q],[r,s]])
# show the results
show(grid)
