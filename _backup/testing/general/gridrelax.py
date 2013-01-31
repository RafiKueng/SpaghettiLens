import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def smooth(A):
  x_dim, y_dim = A.shape
  
  for x in range(1,x_dim-1):
    for y in range(1,y_dim-1):
      A[x,y] = (A[x-1,y]+A[x+1,y]+A[x,y-1]+A[x,y+1]+4*A[x,y])/8.
  return A
  


A = np.ones([60,60])

A[20,20] = 0
A[30,30] = 0.5
A[40,40] = 0.25

maxfac = 10.0

for i in range(1000):
  A=smooth(A)
  A[20,20] = 0
  A[30,30] = 0.5
  A[29,30] = 0.5/maxfac
  A[31,30] = 0.5/maxfac
  A[30,31] = 0.5/maxfac
  A[30,29] = 0.5/maxfac
  #A[40,40] = 0

plt.figure()
CS = plt.contour(A,100)

plt.show()