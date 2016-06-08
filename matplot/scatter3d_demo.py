import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json
from collections import OrderedDict
import matplotlib.pyplot as plt


def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
#for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#    xs = randrange(n, 23, 32)
#    ys = randrange(n, 0, 100)
#    zs = randrange(n, zl, zh)
#    ax.scatter(xs, ys, zs, c=c, marker=m)

#Get data from json file
with open("gps_sd.json") as definitions:
	json_data = json.load(definitions)


# prepare some data, 16 total rows
xs = []
ys = []
zs = []

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

#Traverse the matrix
for i in range(len(bitvalues_2d)):
	for j in range(len(bitvalues_2d[i])):
        	print(bitvalues_2d[i][j])
        	xs.append(i)
        	ys.append(j)
        	zs.append(bitvalues_2d[i][j])

#print zs

#Z axis is the 0 or 1
#Y is bit
#X is the iteration
c = 'r'
m = 'o'

ax.set_ylim3d(0,3)
ax.set_zlim3d(-1,1)
#Set the ticks,steps of 1
ax.yaxis.set_ticks(np.arange(0,4,1.0))
#ax.xaxis.set_ticks(np.arange(0,len(bitvalues_2d)+1,1.0))
ax.zaxis.set_ticks(np.arange(0,2,1.0))
ax.scatter(xs, ys, zs, c=c, marker=m,zdir='z')
#ax.plot(xs,ys,zs)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
