#!/usr/bin/env python
import json
from bokeh.plotting import *
import click
#from bokeh.plotting import figure, output_file, show

#Get data from json file
with open("k64.json") as definitions:
	json_data = json.load(definitions)

# prepare some data
iterations = range(0,len(json_data)-1)
main_loop_counter = []
gps_seconds = []
gps_minutes = []
status = []
heading_degrees = []
heading_raw = []
pitch_deg = []
roll_deg = []
odo_tix = []

for element in json_data:
	main_loop_counter.append(element['main_loop_counter'])
        gps_seconds.append(element['gps_seconds'])
        gps_minutes.append(element['gps_minutes'])
        status.append(element['status'])
        heading_raw.append(element['heading_raw'])
        heading_degrees.append(element['heading_deg'])
        pitch_deg.append(element['pitch_deg'])
        roll_deg.append(element['roll_deg'])
	odo_tix.append(element['odometer_ticks'])
#Remove zero function
def remove_zeros(data):
	if data != 0.0:
		return data

# output to static HTML file
output_file(definitions.name.split(".")[0]+"_lines.html", title="line plot example")

# create a new plot with a title and axis labels
m = figure(title="Main loop counter", x_axis_label='iteration', y_axis_label='count')
gs = figure(title="GPS Seconds", x_axis_label='iteration', y_axis_label='Seconds')
gm = figure(title="GPS Minutes", x_axis_label='iteration', y_axis_label='Minutes')
s = figure(title="Status", x_axis_label='iteration', y_axis_label='Status')

p = figure(title="Raw Heading", x_axis_label='iteration', y_axis_label='10th Degrees')
q = figure(title="Heading in Degrees", x_axis_label='iteration', y_axis_label='Degrees')
r = figure(title="Pitch in Degrees", x_axis_label='iteration', y_axis_label='Degrees')
rd = figure(title="Roll in Degrees", x_axis_label='iteration', y_axis_label='Degrees')
odo = figure(title="Odometer", x_axis_label='iteration', y_axis_label='Ticks')


# add a line renderer with legend and line thickness
m.line(iterations, main_loop_counter, legend="Main loop", line_width=2)
gs.line(iterations, filter(remove_zeros,gps_seconds), legend="GPS Seconds", line_width=2)
gm.line(iterations, filter(remove_zeros,gps_minutes), legend="GPS Minutes", line_width=2)
s.line(iterations, filter(remove_zeros,status), legend="Status", line_width=2)
p.line(iterations, heading_raw, legend="Heading Raw", line_width=2)
q.line(iterations, heading_degrees, legend="Heading degrees", line_width=2)
r.line(iterations, pitch_deg, legend="Pitch Degrees", line_width=2)
rd.line(iterations, roll_deg, legend="Roll Degrees", line_width=2)
odo.line(iterations,odo_tix,legend="Odometer Ticks", line_width=2)


grid = gridplot([[m,s],[gm,gs],[p,q],[r,rd],[odo]])
#grid = gridplot([[p,q],[r,s]])
# show the results
show(grid)
#show(m)
#@click.command()
#@click.option('--d',default='definitions.json',help='Definitions file as json')
#def main(i)
