#!/usr/bin/env python
 
import sys
import json
import subprocess

from twisted.internet import reactor
from twisted.python import log
from time import sleep

 
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
 
run_id=0
 

class GlassSettings(object):
  def __init__(self, lensid, runid):
    self.lens_id = lensid #expected to be a string
    self.run_id = repr(runid)
    self.points = []
    
  
  #add them in the right order! fifo
  def addSource(self, point):
    self.points.append(point)
  
  def setRedshiftLens(self, z):
    self.zlens = z
    
  def setRedshiftSource(self, z):
    self.zSrc = z
  
  
  def genOutput(self):
    s = self
    out = """
import matplotlib as mpl
#mpl.use('Agg') #make plots on headless server 
#import matplotlib.pyplot as pl
import pylab as pl

glass_basis('glass.basis.pixels', solver='rwalk')
meta(author='Jonathan Coles', notes='Just testing')
"""
    out += "setup_log('" + s.lens_id + "_" + s.run_id + ".log')\n"
    
    out += """
samplex_random_seed(0)
samplex_acceptance(rate=0.25, tol=0.15)

exclude_all_priors()
include_prior(
    'lens_eq', 
    'time_delay', 
    'profile_steepness', 
    'J3gradient', 
    'magnification',
    'hubble_constant',
    'PLsmoothness3',
    'shared_h',
    'external_shear'
)

hubble_time(13.7)
"""

    out += "globject('" + s.lens_id + "')\n"
    out += "zlens(" + s.zlens + ")\n"
    out += """
pixrad(3) 
steepness(0,None)
smooth(2,include_central_pixel=False)
local_gradient(45)
shear(0.01)

"""
    
    for i in range(len(s.points)):
      out += chr(65+i) + " = " + s.points[i].toStringA() + "\n"
    
    out += "\nsource(" + s.zSrc + ", \n"
    
    for i in range(len(s.points)):
      out += chr(65+i) + ", " + s.points[i].toStringB() + (",\n" if i < len(s.points)-1 else ")\n\n")
      
    out += "model(1000)\n"
    
    s.statefile = s.lens_id + "_" + s.run_id + ".state"
    out += "savestate('../tmp/" + s.statefile + "')" 
    
    out += """ 


#pl.figure()
#env().glerrorplot('kappa(R)', ['R', 'arcsec'])
#pl.savefig('kappa_R.png')
env().make_ensemble_average()
env().arrival_plot(env().ensemble_average, only_contours=True)
""" 
    s.imgfile = s.lens_id + "_" + s.run_id + ".png"
    out += "pl.savefig('../htdocs/img/" + s.imgfile + "')"
 
     
    s.cfgfile = s.lens_id + "_" + s.run_id + ".gls"
    f = open('../tmp/' + s.cfgfile, 'w')
    f.write(out)
    f.close()

    
  

class Point(object):
  def __init__(self, x,y,type='None',delay='None'):
    self.x = x
    self.y = y 
    self.type = type
    self.delay = 'None' if delay=='' else delay 
    print "creating point: ", "XX" if delay==None else delay 
   
  def toStringA(self):
    return self.x+','+self.y
    
  def toStringB(self):
    return "'" + self.type + "' " + ('' if self.delay==None else ', '+self.delay)
  
 
class EchoServerProtocol(WebSocketServerProtocol):

  def onOpen(self):
    print "-------\nnew connection"
    
  def onClose(self, wasClean, code, reason):
    print "closed connection"
 
  def onMessage(self, msg, binary):

    print "got message: ", msg
    
    id = msg[0:4] 
    data = msg[4:]
    
    if (id == "p_id"):
      try:
        p_id = int(data)
      except ValueError:
        print "got invalid p_id, sending error"
        self.sendMessage("err_" + "invalid p_id")
        return
        
      print "got p_id: " + data
      
      if (p_id==1):
        url = "hubble-udf.jpg"
      elif (p_id==2):
        url = "http://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Einstein_cross.jpg/621px-Einstein_cross.jpg"
      elif (p_id==3):
        url = "demo-gray.png"
      elif (p_id==4):
        url = "DEVDEMO"
      else:
        url = "no-img.jpg"
      self.sendMessage("limg" + url)
      print "send limg: " + url
    
    elif (id=="pnts"):
      print "got pnts: " + data
      
      #read in the points
      data = [_.split(':') for _ in data.split('|')]
       
      global run_id
      run_id += 1 
      gs = GlassSettings(data[0][0],run_id)
      
      for i in range(1,len(data)-1):
        if len(data[i])==4:
          delay = data[i][3]
        elif i==1: 
          delay = None
        else:
          delay = ''
        
        print "got data: ", i, len(data[i]), data[i][0], data[i][1], data[i][2], repr(delay)
        pnt = Point(data[i][0], data[i][1], data[i][2], delay)
        gs.addSource(pnt) 
        
      #the last line are the other parameters
      gs.setRedshiftLens(data[-1][0])
      gs.setRedshiftSource(data[-1][1])      
      
      gs.genOutput() 
         
      #call glass, generate img
      print "call glass"
      retval = subprocess.call(['../glass/run_glass', '../tmp/'+gs.cfgfile]) 
      print "return from glass with:", retval
      self.sendMessage("stat" + repr(retval)) 
       
      #subprocess.call(['../glass/run_glass', '../tmp/'+gs.cfgfile])
      #sleep(10) #wait for glass to finish 
      #if retval==0:
      url = 'img/' + gs.imgfile
      self.sendMessage("cont" + url)
      #else:
        #self.sendMessage("stat" + "ERROR IN GLASS")
      
    else:
      print "PROTOCOLL ERROR - dump:"
      print msg

  def prepareGlassInputFile():
    pass
  
if __name__ == '__main__':

  # print "testing"
  # gs = GlassSettings(1,1)
  # pnt = Point(4.3,5.4,'min',None)
  
  # gs.addSource(pnt)
  # gs.addSource(pnt)
  # gs.addSource(pnt)
  # gs.setRedshiftLens(0.5)
  # gs.setRedshiftSource(1)
  # gs.genOutput()  
    

  log.startLogging(sys.stdout)

  factory = WebSocketServerFactory("ws://localhost:8080", debug = False)
  factory.protocol = EchoServerProtocol
  listenWS(factory)

  reactor.run()
