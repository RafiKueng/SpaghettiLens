#!/usr/bin/env python

import sys
import re
import numpy as np

regexes = [
  re.compile('Pixel radius\s+=\s*(\d+)'),
  re.compile('Number of pixels\s+=\s*(\d+)'),

  re.compile('Number of CPUs detected\s+=\s*(\d+)'),
  re.compile('Number of CPUs used\s+=\s*(\d+)'),

  re.compile('burn-in length\s+=\s*(\d+)'),
  
  re.compile('Generated (\d+) model'),
  
  re.compile('Initial inner point\s*(\d*.\d*)'),
  re.compile('Estimate eigenvectors\s*(\d*.\d*)'),
  re.compile('Burn-in\s*(\d*.\d*)'),
  re.compile('Modeling\s*(\d*.\d*)'),
  re.compile('Max/Avg thread time\s*\d*.\d*s\s(\d*.\d*)'),
  re.compile('Total wall-clock time\s*(\d*.\d*)'),
]
modnr = re.compile('\d+')

mlregs = [
  re.compile('B THREAD .*time\s(\d+.\d*)s'),
  re.compile('THREAD .*time\s(\d+.\d*)s\s+\d+\sleft\.'),
]

#print 'args: ', sys.argv

l1=len(regexes)
l2=len(mlregs)
j=0

for arg in sys.argv[1:]:
  j+=1  
  if j>10:break
  #print arg
  with open(arg, 'r') as file:
    txt = file.read()
    res = np.zeros(2+l1+l2)
    res[1] = 1
    
    res[0] = modnr.search(arg).group()
    
    for i, regex in enumerate(regexes):
      try:
        res[i+2] = regex.search(txt).groups()[0]
      except AttributeError:
        res[1] = 0
        #res[i+1] = -1
    
    for i, regex in enumerate(mlregs):
      try:
        l = regex.findall(txt)
        m = np.array(l, dtype=np.float32)
        a = np.average(m)
        res[i+l1+2] = a
      except:
        res[1] = 0
        #res[i+l1+1] = -1
        
    #print ', '.join(map(str,res))
    print '%4i, %1i, %2i, %4i, %1i, %1i, %4i, %4i, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %5.3f, %5.3f' % tuple(map(float,res))
