from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')


def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)


def bit_vertices(start_x,length,bit):
    verts = []
    #First vertice for our polygon
    verts.append((start_x,0))
    #Second and third
    if bit == 1:
        #Second vertice
        verts.append((start_x,1))
        #Third, moves the x over by length
        verts.append((start_x+length,1))
    else:
        verts.append((start_x,0))
        verts.append((start_x+length,0))
    #Fourth is always the same
    verts.append((start_x+length,0))
    return verts

def bitstring_vertices(bitstring,start_x):
    verts = []
    for n in bitstring:
        #length , the width of the "bit" on the polygon
        #we're going through each bit
        bit_vert = bit_vertices(start_x,1,n)
        start_x = bit_vert[-1][0]
        #print start_x
        verts.extend(bit_vert)
    return verts



#xs = np.arange(0, 10, 0.4)
#print xs

#verts = []
#zs = [0.0, 1.0, 2.0, 3.0]
#for z in zs:
#    ys = np.random.rand(len(xs))
#    ys[0], ys[-1] = 0, 0
#    verts.append(list(zip(xs, ys)))

#print verts

bitstrings = [
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


verts = [bitstring_vertices(n,-0.5) for n in bitstrings]
print verts[0]
print verts[1]
print verts[2]
zs = range(0,len(bitstrings))

color_choices = ['r','g','b','y']
colors = [cc(color_choices[x%4]) for x in range(len(bitstrings)) ]

#print verts
#poly = PolyCollection(verts, facecolors=[cc('r'), cc('g'), cc('b'),cc('y')])
poly = PolyCollection(verts, facecolors=colors)

poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=zs, zdir='y')

ax.set_xlabel('bit')
#X limit is the byte length
ax.set_xlim3d(-1, len(bitstrings[0]))

ax.set_ylabel('Iteration')
ax.set_ylim3d(0, len(bitstrings))
ax.set_zlabel('Z')
ax.set_zlim3d(0, 1)

plt.show()
