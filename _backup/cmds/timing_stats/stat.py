import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.pyplot as plt
 
pixrad = []
nmods = []
time = []

with open('timings.csv', 'r') as csvfile:
  csvf = csv.reader(csvfile)
  csvf.next()
  for line in csvf:
    #print line
    pixrad.append(np.float64(line[1]))
    nmods.append(np.float64(line[2]))
    time.append(np.float64(line[3]))


def func(p,a1,a2, a3):
  s = p*a2
  t = np.exp(s)
  return a1*t+a3
    
p = np.array(pixrad, dtype = np.float64)
t = np.array(time, dtype = np.float64)

res = curve_fit(func, p, t)

plt.plot(p, t, '.')
i=0

print res[i]

x = np.linspace(4,14)
y = func(x, res[i][0], res[i][1], res[i][2])
plt.plot(x, y)

print x
print y
plt.ylim([-1,50])

plt.show()



def func(n, a, b):
  return a*n+b

n = np.array(nmods, dtype = np.float64)
t = np.array(time, dtype = np.float64)

res = curve_fit(func, n, t)

plt.plot(n, t, '.')
i=0

print res[i]

x = np.linspace(50,2000)
y = func(x, res[i][0], res[i][1])
plt.plot(x, y)
plt.show()
