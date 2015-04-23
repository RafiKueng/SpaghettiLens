from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from pylab import figure, show
from numpy import linspace, meshgrid, sin, log

fig = figure()
fig.patch.set_facecolor('black')
ax = fig.gca(projection='3d')
ax.patch.set_facecolor('black')

rmax = 0.6
X = linspace(-rmax,rmax,60)
Y = 1*X
X, Y = meshgrid(X, Y)
zmax = 1
zmin = -0.5  

R = (X**2 + Y**2)**.5
g = ((X-.03)**2 + Y**2)**.5
Z = sin(R)**2 - log(g+0.01)*0.3 + 0.2*X*Y

ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])
ax.zaxis.set_ticks([])

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='cyan', # cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
 
cset = ax.contour(X, Y, Z, 100, zdir='z', offset=zmin, cmap=cm.coolwarm)


ax.set_zlim(zmin, zmax)
#fig.colorbar(surf, shrink=0.5, aspect=5)
show()

