import numpy as np
import matplotlib.pyplot as pl
import scipy.integrate as spi

c = 1.0 # Canonical coordinates?
rs = .20 # No reason, is there? Just a nice number

def deriv(y,s):
  return np.array([
    y[4], y[5], y[6], y[7],
    rs*0.5/y[0]/(y[0]-rs)*y[4]**2 + (y[0]-rs)*y[5]**2 + (y[0]-rs)*np.sin(y[1])**2*y[6]**2 + c*c*rs*(rs-y[0])*0.5/y[0]**3*y[7]**2,
    -2.0/y[0]*y[4]*y[5] + np.sin(y[1])*np.cos(y[1])*y[6]**2,
    -2.0/y[0]*y[4]*y[6] - 2.0/np.tan(y[1])*y[5]*y[6],
    rs/y[0]/(rs-y[0])*y[4]*y[7]
  ])


fig = pl.figure(1)

for ang in np.linspace(-np.pi/32.,np.pi/32.,32):

  # Initial conditions
  x0r = np.array([ -10, 0, 0.0])
  #x0rd= np.array([ 0.0, y0, 0.0])
  x0rd= np.array([ 1.0*np.cos(ang), 1.0*np.sin(ang), 0.0])

  # Convert the initial position to spherical coordinates
  x0 = np.zeros(3)
  x0[0] = np.sqrt(x0r[0]**2+x0r[1]**2+x0r[2]**2)
  x0[1] = np.arccos(x0r[2]/x0[0])
  x0[2] = np.arctan2(x0r[1],x0r[0])

  # Convert the initial velocity to spherical coordinates
  x0d = np.array([
     np.cos(x0[2])*np.sin(x0[1])      *x0rd[0] + np.sin(x0[2])*np.sin(x0[1])      *x0rd[1] + np.cos(x0[1])      *x0rd[2],
     np.cos(x0[2])*np.cos(x0[1])/x0[0]*x0rd[0] + np.sin(x0[2])*np.cos(x0[1])/x0[0]*x0rd[1] - np.sin(x0[1])/x0[0]*x0rd[2],
    -np.sin(x0[2])/np.sin(x0[1])/x0[0]*x0rd[0] + np.cos(x0[2])/np.sin(x0[1])/x0[0]*x0rd[1]
  ])

  # Pack the initial conditions into an array
  y0 = np.array([  x0[0],  x0[1],  x0[2], 0.0, x0d[0], x0d[1], x0d[2], 1.0 ])

  # Parameterized time intervals
  s = np.linspace(0,20,100000)

  # Integrate
  y = spi.odeint( deriv, y0, s )

  dt = 100
  # Unpack the results
  r = y[::dt,0]
  theta = y[::dt,1]
  phi = y[::dt,2]
  t = y[::dt,3]

  if False:
    r = y[:,0]
    theta = y[:,1]
    phi = y[:,2]
    t = y[:,3]

  # Plot in the equatorial plane
  pl.plot(r*np.cos(phi),r*np.sin(phi),)


ax = pl.gca()
ax.add_patch( pl.Circle((0,0), radius=rs, fc=[0,0,0]))
pl.axis([-5,5,-5,5])
ax.set_aspect(1)
pl.show()
