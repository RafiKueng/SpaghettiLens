from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

#mpl.use("Agg")

from matplotlib import cm
from pylab import figure, show, savefig
from numpy import linspace, meshgrid, sin, log


rmax = 0.6
X = linspace(-rmax,rmax,60)
Y = 1*X
X, Y = meshgrid(X, Y)
zmax = 1
zmin = -0.5  

R = (X**2 + Y**2)**0.5
S1 = ((X+0.2)**2 + (Y-0.2)**2)**0.5
S2 = ((X-0.2)**2 + (Y+0.2)**2)**0.5
g = ((X-.03)**2 + Y**2)**.5
h = ((X)**2 + Y**2)**.5
Z = [0,0,0,0,0]
Z[0] = sin(R)**2 #- (g+0.01)*0.01 + 0.2*X*Y
Z[1] = sin(R)**2 - log(g+0.01)*0.3 + 0.2*X*Y
Z[2] = sin(R)**2 - log(h)*0.3
Z[3] = sin(R*1.5)**2 - log(g)*0.3
Z[4] = (S1*S2)**0.5

doplot = range(len(Z))
#doplot = [3]

for i in doplot:

  print "figure", i

  fig = figure(figsize=(10.24, 7.2)) #go for 1200x720 with 100dpi
  fig.patch.set_facecolor('black')
  ax = fig.gca(projection='3d')
  ax.patch.set_facecolor('black')

  ticks = [-0.5,0,0.5]
  ticks = []
  zticks = [0,0.25,0.5]
  zticks = []
  
  ax.xaxis.set_ticks(ticks)
  ax.yaxis.set_ticks(ticks)
  ax.zaxis.set_ticks(zticks)

  col2 = (0.9,)*3
  ax.tick_params(axis='x', colors=col2)
  ax.tick_params(axis='y', colors=col2)
  ax.tick_params(axis='z', colors=col2)
  
  surf = ax.plot_surface(X, Y, Z[i], rstride=1, cstride=1, 
    cmap=cm.coolwarm,
    #color="cyan",
    linewidth=0, antialiased=True)
   
  cset = ax.contour(X, Y, Z[i], 50, zdir='z', offset=zmin, cmap=cm.coolwarm)
  #ax.clabel(cset, fontsize=9, inline=1)
  
  col= 0.2
  ax.w_xaxis.set_pane_color((col, col, col, 1.0))
  ax.w_yaxis.set_pane_color((col, col, col, 1.0))
  ax.w_zaxis.set_pane_color((col, col, col, 1.0))
  
  ax.set_xlabel('X Direction')
  ax.set_ylabel('Y Direction')
  ax.set_zlabel('Arrival Time')
  ax.xaxis.label.set_color("white")
  ax.yaxis.label.set_color("white")
  ax.zaxis.label.set_color("white")

  ax.set_zlim(zmin, zmax)
  #fig.colorbar(surf, shrink=0.5, aspect=5)
  #show()
  #savefig('fig'+str(i)+'.png', dpi=100)
  savefig('fig'+str(i)+'.eps')

