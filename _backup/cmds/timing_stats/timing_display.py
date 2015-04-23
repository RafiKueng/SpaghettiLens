from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np






fig = plt.figure()
ax = fig.gca(projection='3d')
pixelradius = np.arange(4, 15, 0.25)
n_models = np.arange(50, 3000, 25)

pixelradius, n_models = np.meshgrid(pixelradius, n_models)

Z = (0.108 * np.exp(0.506*pixelradius) + 0.01 * n_models + 0.5) # * 3 + 30

steps = Z*0
ds = 10
for i in np.arange(0,100,ds):
  steps += Z>i
steps *= ds

surf = ax.plot_surface(pixelradius, n_models, steps, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=True)
#ax.set_zlim(-1.01, 1.01)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()