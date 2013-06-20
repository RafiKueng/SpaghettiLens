from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

mpl.use("Agg")

from matplotlib import cm
from pylab import figure, show, savefig
from numpy import linspace, meshgrid, sin, log


rmax = 0.6
X = linspace(-rmax,rmax,60)
Y = 1*X
X, Y = meshgrid(X, Y)
zmax = 1
zmin = -0.5  

R = (X**2 + Y**2)**.5
g = ((X-.03)**2 + Y**2)**.5
h = ((X)**2 + Y**2)**.5
Z = [0,0,0,0,0]
Z[0] = sin(R)**2 - (g+0.01)*0.01 + 0.2*X*Y
Z[1] = sin(R)**2 - log(g+0.01)*0.3 + 0.2*X*Y
Z[2] = sin(R)**2 - log(h)*0.3
Z[3] = sin(R)**2 - log(g+0.01)*0.3 + 0.8*X*Y
Z[4] = sin(R)**2 - log(g)*0.3 + 0.8*X*Y

for i in [4]:

  print "figure", i

  fig = figure(figsize=(12.8, 7.2)) #go for 1200x720 with 100dpi
  ax = fig.gca(projection='3d')

  ax.xaxis.set_ticks([])
  ax.yaxis.set_ticks([])
  ax.zaxis.set_ticks([])

  surf = ax.plot_surface(X, Y, Z[i], rstride=1, cstride=1, cmap=cm.coolwarm,
          linewidth=0, antialiased=False)
   
  cset = ax.contour(X, Y, Z[i], 100, zdir='z', offset=zmin, cmap=cm.coolwarm)


  ax.set_zlim(zmin, zmax)
  fig.colorbar(surf, shrink=0.5, aspect=5)
  #show()
  savefig('fig'+str(i)+'.png', dpi=100)

