#!/usr/bin/env python

import sys
import re


regexes = [
  re.compile('Pixel radius\s+=\s*(\d+)'),
  re.compile('Generated (\d+) model'),
  re.compile('Total wall-clock time\s*(\d*.\d*)'),
  re.compile('Modeling\s*(\d*.\d*)')
]
modnr = re.compile('\d+')
  
#print 'args: ', sys.argv
for arg in sys.argv[1:]:
  #print arg
  with open(arg, 'r') as file:
    txt = file.read()
    res = [modnr.search(arg).group(),'','','','']
    try:
      for i, regex in enumerate(regexes):
        res[i+1] = regex.search(txt).groups()[0]
      print res
    except AttributeError:
      print res[0], '---------------'
  



