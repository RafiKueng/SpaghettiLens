#from ModellerApp.models import ModellingResult, ModellingSession
from django.conf import settings

import json
import os
from attrdict import AttrDict
import numpy as np

class Point(object):
  def __init__(self, x, y, _type='min', _delay="", child1=None, child2=None, wasType=""):
    self.x = x
    self.y = y
    self.child1 = child1
    self.child2 = child2
    self.type = _type
    self.wasType = wasType
    self.delay = _delay #either float in days, or empty string for None (messured)
    self.distParent2 = -1 #init to no parent, if it has one, the parent will change this setting
    
    #save distance to parent for children
    for child in [child1, child2]:
      if child:
        dx = child.x - self.x
        dy = child.y - self.y
        child.distParent2 = dx*dx+dy*dy
  
  '''get the dist squarred to another point like obj'''
  def getDist2To(self, other):
    dx = other.x - self.x
    dy = other.y - self.y
    return dx*dx+dy*dy
    
  '''calculates the relative coordinates to another point, returns a new point'''
  def getRelCoordTo(self, pnt):
    dx = self.x - pnt.x
    dy = self.y - pnt.y
    #print " "*30, "in new point: ", self.type, self.wasType
    return Point(x=dx, y=dy, _type=self.type);
  
  '''rescales the values from px to arcsec'''
  def changePxToArcsec(self, pxScale):
    f = pxScale
    self.x *= f
    self.y *= -f
    

  def __repr__(self):
    return "Point [ x:% .2f | y:% .2f | type:%s ]" % (self.x, self.y, self.type)
  def __str__(self):
    return self.__repr__()
    
  def toDict(self):
      return {
        'x': self.x,
        'y': self.y,
        'type': self.type,
        'wasType': self.wasType,
        'delay' : self.delay
      }
      
  def toGLSLst(self, i):
      if i == 0:
          return [[self.x, self.y], self.type]
      else:
          return [[self.x, self.y], self.type, None]
          


'''
represents an external mass
m, m_min, m_max stand for the Mass in units of einsteinradius! arcsec!!
derr1: if m supllied, allow m to variate between m*(1-derr) and m*(1+derr)
  0.1 -> 10% -> 0.9*m ... 1.1*m
derr2: if m supllied, allow m to variate between m*(1/derr) and m*(1*derr)
  2  -> 1/2 * m ... 2 * m
'''
class ExtMass(object):
  #def __init__(self, x, y, id=-1, m=None, m_min=None, m_max=None, derr=None, derr2=None):
  def __init__(self, x_px, y_px, id=-1, m_px=None,
               m_px_min=None, m_px_max=None, derr1=None, derr2=None):
    self.id = id
    self.x_px = x_px
    self.y_px = y_px

    self.m_px = m_px
    self.m_px_min = m_px_min
    self.m_px_max = m_px_max
    self.derr1 = derr1
    self.derr2 = derr2
    
    self.x = self.y = self.m = self.m_min = self.m_max = None
    
    self.init = False

  def getStr(self):
    _=self
    if not _.init: return ""
    rstr = ''
    if not _.m and not _.m_min and not _.m_max:
      rstr=""
    elif _.m:
      rstr = ",%.6f" % _.m
    else:
      rstr = ",[%.6f,%.6f]" % (_.m_min, _.m_max)
    return "external_mass(PointMass(%.4f,%.4f,name='PM%i')%s)" % (_.x, _.y, _.id, rstr)
        
  def __repr__(self):
    _=self
    mstr = ''
    if not _.m_px and not _.m_px_min and not _.m_px_max:
      mstr="None"
    elif _.m_px:
      mstr = "%.6f" % _.m_px
    else:
      mstr = "[%.6f,%.6f]" % (_.m_px_min, _.m_px_max)

    str = "ExtPointMass [ nr:%i | x_px:%.2f | y_px:%.2f | m_px:%s ]" % (self.id, self.x_px, self.y_px, mstr)

    if _.init:
      rstr = ''
      if not _.m and not _.m_min and not _.m_max:
        rstr="None"
      elif _.m:
        rstr = "%.6f" % _.m
      else:
        rstr = "[%.6f,%.6f]" % (_.m_min, _.m_max)
      return str + "[ x:% .3f | y:% .3f | m:%s ]" % (self.x, self.y, rstr)
    else:
      return str
  
  def __str__(self):
    return self.__repr__()

  # changes the pixel values to relative values
  # and the massses/radius to arcsec
  # note: origin is and stays in pixels!!

  #TOODO clean this up! limits not working any more correctly, only mode with one numer (= will be interpretes as upper limit)
  def changePxToArcsec(self, origin, pxScale):

    # rescale the location
    self.x = (self.x_px - origin.x) *  1.0 * pxScale
    self.y = (self.y_px - origin.y) * -1.0 * pxScale

    # convert the radius in px to mass in arcsec
    #f = 1.0 * viewport/imgSize * pxScale
    f = pxScale

    r     = self.m_px*f     if self.m_px     else None 
    m_min = self.m_px_min*f if self.m_px_min else None 
    m_max = self.m_px_max*f if self.m_px_max else None 

    m = r**2 * np.pi

    if not m_min and not m_max and m: #-1 or None
      if self.derr1:
        self.m = None
        self.m_min = m*(1.-derr1)
        self.m_max = m*(1.+derr1)
      elif self.derr2:
        self.m = None
        self.m_min = m*(1./derr2)
        self.m_max = m*(1.*derr2)
      else:
        self.m = m
        self.m_min = None
        self.m_max = None
        
    elif not m and m_min and m_max:
      self.m = None
      self.m_min = m_min
      self.m_max = m_max
    else:
      self.m = None
      self.m_min = None
      self.m_max = None
    
    self.init = True
    return self
    
    
  def toDict(self):
      return {
        'x': self.x,
        'y': self.y,
        'm': self.m #* 1e-6, #TODO fix this
      }



class EvalAndSaveJSON:
  
  def __init__(self, user_str, data_obj, jsonStr, is_final, prefs={}):
      
    self._ = AttrDict()
#    _ = self.obj

    #print "init easj"
    #self.username = "anonymous"
    self._.hubbletime = 13.7
    self._.z_lens = 0.50
    self._.pixrad = 5
    self._.steep_min = 0 #TODO remove by steepness
    self._.steep_max = "None" #TODO remove by steepness
    self._.smooth_val = 2
    self._.smooth_ic = "False" #TODO is overwritten below
    self._.loc_grad = 45
    self._.isSym = False
    self._.maprad = 0 #1.9637 #set 0 to turn off
    self._.shear = 0.10  # new default value is 10 times bigger
    self._.z_src = 1.00
    self._.n_models = 200
    
    self._.viewport = 500   # viewport size default in <GLSv3, LMTv1.6
    self._.imgSize  = 440   # default for spacewarps
    self._.pxScale  = 0.01  # default [LMT] viewport pixel coordinates -> [glass] arcsec; [arcsec / px]
    self._.orgPxScale = 0   # orgImg: arcsex / px

    #newly added params
    self._.random_seed = 0
    self._.author = "[none]"
    self._.notes = ""
    self._.samplex_acceptance = {'rate':0.25, 'tol':0.15}
    self._.exclude_all_priors = True
    self._.include_priors = ['lens_eq', 'time_delay', 'profile_steepness', 'J3gradient', 
                           'magnification', 'hubble_constant', 'PLsmoothness3', 'shared_h',
                           'external_shear'
                           ]
    self._.steepness = [0, None]
    self._.smooth_ic = False

    #self.points = [Pnt(2,3), Pnt(2,1), Pnt(5,2)]  

    #replacce default settings with setttings provided
    for key, value in prefs.iteritems():
      if hasattr(self._, key):
        setattr(self._, key, value)
      
    #save databse elements / objects
    self._.lens_data_obj = data_obj._id
#    self._.user_str = user_str
    self._.author = user_str
    self._.jsonStr = jsonStr
    self._.is_final = is_final
    
    
    
    # lets got to work
    #print "EAS: eval"
    self.evalModelString()
    #print "EAS: oder"
    self.orderPoints2()
#    print "EAS: create mr"
#    self.createModellingResult()
#    print "EAS: create cfg"
    self.createConfigFile()    
    #print "EAS: done"
        
#  def __setitem__(self, key, value):
#    self.__dict__[key] = value
  def __setitem__(self, key, value):
    self._[key] = value
    
  def evalModelString(self):
    #print "eval easj"
    
    def objHook(dct):
      #print "in ObjHook"
      if '__type' in dct:
        if dct['__type'] == "extpnt":
          #return Point(x=dct['x']/100., y=dct['y']/(-100.), _type=dct['type'], child1=dct['child1'], child2=dct['child2'], wasType=dct['wasType'])
          return Point(x=dct['x'], y=dct['y'], _type=dct['type'], child1=dct['child1'], child2=dct['child2'], wasType=dct['wasType'])
        if dct['__type'] == "contour":
          return None
        if dct['__type'] == "cpnt":
          return None
        if dct['__type'] == "ext_mass":
          return ExtMass(id=dct['idnr'], x_px=dct['x'], y_px=dct['y'], m_px=dct['r'])
        if dct['__type'] == "ruler":
          return None
      return dct
        
    self._.jsonObj = json.loads(self._.jsonStr, object_hook=objHook)
    
    #print "converted json str"
    #print self._.jsonObj
    
    gs = self._.jsonObj["Parameters"]
    

    # make sure to check the passed parameters and to cast it to expected types, to prevent script injection
    glassParameter = {'hubbletime': float,
                      'z_lens': float,
                      'pixrad': int,
                      'steep_min': float,
                      'steep_max': str,
                      'smooth_val': int,
                      'smooth_ic': str,
                      'loc_grad': int,
                      'isSym': bool,
                      'maprad': float,
                      'shear': float,
                      'z_src': float,
                      'n_models': int,
                      
                      'svgViewportSize': int, # viewport size of svg window in pixel, needed for px - arcsec conversion
                      'orgImgSize': int,  # original image size, same here
                      'orgPxScale': float,  # orgImg arcsec / px
                      'pxScale': float}  # viewport arcsec / px
    
    for attr, type in glassParameter.iteritems():
      #print "trying ", attr, ":",  attr in r
      if attr in gs:
        if type == bool:
          value = gs[attr] in ["True", "true", True, 1]
        else: #TODO: check for null values
          try:
            value = type(gs[attr])
          except TypeError:
            value = 0
        #print "found attr:", attr, str(type), ":", value, gs[attr] 
        self._[attr] = value
        
    #self.isSym = True;
    
    #return self.jsonObj
  
  
  
  
  def orderPoints2(self):
    # find origin first
    pnt = self._.jsonObj['Sources'][0] #TODO: here is hardcoded that only the fors soucre is supported
    
    # note: origin is and stays in pixels!!
    try:
      origin = pnt
      for child in [pnt.child1, pnt.child2]:
        if child.type == "max" or child.wasType == "max":
          origin = child
          break
      
    except: # this source doen't have any children
      return [pnt]

    
    
    def recWalker(pnt, origin, depth=0, level=0):
      res = []
      #a = " "*(depth*3)
      #print a, "rec:", level, pnt.x, pnt.y, pnt.type, pnt.wasType
      
      try:
        ch1type = pnt.child1.wasType if pnt.child1.type == "sad" else pnt.child1.type
        ch2type = pnt.child2.wasType if pnt.child2.type == "sad" else pnt.child2.type
        
        if (ch1type == ch2type):
          d1 = (1.0 if ch1type == "max" else -1.0)
          d2 = d1
          v = pnt.getDist2To(pnt.child1) / pnt.getDist2To(pnt.child2)
          if v >= 1:
            d2 /= v
          else:
            d1 *= v
        else:
          d1 = (1.0 if ch1type == "max" else -1.0)
          d2 = d1 * (-1.0)
        
        d1 /= depth
        d2 /= depth
        #print a, "next walker: ch1:"
        res.extend(recWalker(pnt.child1, origin, depth=depth+1, level = level+d1))
        #print a, "next walker: ch2:"
        res.extend(recWalker(pnt.child2, origin, depth=depth+1, level = level+d2))
      except:
        #print " "*(depth*3), "no children"
        pass
      #print a, "get new point:"
      npnt = pnt.getRelCoordTo(origin)
      npnt.level = level
      npnt.depth = depth
      #print a, "-> ", npnt.x, npnt.y, npnt.type, npnt.level
      res.append(npnt)
      return res
      
      
    res = recWalker(pnt, origin, depth=1, level=0)
    res.sort(key=lambda pnt: pnt.level)
    #print "sorted"
    for r in res:
      r.changePxToArcsec(self._.pxScale)
      #print r, "-> x:% .2f, y:% .2f, type:%s, level:% .2f, depth:%i" % (r.x, r.y, r.type, r.level, r.depth)
      
    # if the last point is a max, take it out
    if res[-1].type == "max":
      res = res[:-1]
    self._.points = res
    
    # rescale and set the external masses
    #print 'adding external masses'
    #print 'origin:', origin
    self._.ext_masses = []
    for mass in self._.jsonObj["ExternalMasses"]:
      # note: origin is and stays in pixels!!
      self._.ext_masses.append(mass.changePxToArcsec(origin, self._.pxScale))
      #print mass
   
  
  
  def createConfigFile(self):
    #print "in cfg: start"
    #print self.result_id
    self._.result_id = 000000

    self._.logfilename = "../tmp_media/%06i/log.txt" % self._.result_id
    try:
      cat_name = "__" + str(self.lens_data_obj.catalog.name)
    except:
      cat_name = ""
#    self.lensidentifier = str(self.result_id) + "__" + str(self.lens_data_obj.name) + cat_name
    self._.lensidentifier = "lensidddd"
    self._.statefilepath = "../tmp_media/%06i/state.txt" % self._.result_id
    self._.imgpath = "../tmp_media/%06i/" % self._.result_id
    self._.img_name = "img%i.png"
    
    self._.cfg_path = "../tmp_media/%06i/" % self._.result_id
    self._.cfg_file = "cfg.gls"

    self._.cfg_path = "/tmp/" # % self.result_id
    self._.cfg_file = "cfg.gls"


    _ = self._
    
    #print "start gls"
    
    gls = [
#      "# LMT_GLS_%s" % settings.GLS_VERSION ,
#      "# LMT_%s" % settings.LMT_VERSION ,
      "import matplotlib as mpl"                                            ,
      "import pylab as pl"                                                  ,
      "glass_basis('glass.basis.pixels', solver='rwalk')"                   ,
#      "meta(author='%s', notes='using LensModellingTools')" % _.user_str    ,
      "meta(author='%s', notes='using LensModellingTools')" % 'some user'    ,
      "setup_log('%s')" % _.logfilename                                     ,
      "samplex_random_seed(0)"                                              ,
      "samplex_acceptance(rate=0.25, tol=0.15)"                             ,
      "exclude_all_priors()"                                                ,
      "include_prior("                                                      ,
      "  'lens_eq',"                                                        , 
      "  'time_delay',"                                                     , 
      "  'profile_steepness',"                                              , 
      "  'J3gradient',"                                                     ,
      "  'magnification',"                                                  ,
      "  'hubble_constant',"                                                ,
      "  'PLsmoothness3',"                                                  ,
      "  'shared_h',"                                                       ,
      "  'external_shear',"                                                 ,
      ]
    
    if _.ext_masses:
      gls.append("  'external_mass',")
      
    gls.extend([
      ")"                                                                   ,
      "hubble_time(%f)" % _.hubbletime                                      ,
      "globject('%s')" % _.lensidentifier                                   ,
      "zlens(%.3f)" % _.z_lens                                              ,
      "pixrad(%i)" % _.pixrad                                               ,
      "steepness(%s,%s)" %(_.steep_min, _.steep_max)                        ,
      "smooth(%.2f,include_central_pixel=%s)" % (_.smooth_val, _.smooth_ic) ,
      "local_gradient(%.2f)" % _.loc_grad                                   ,
      "symm()" if _.isSym else ""                                           ,
      "maprad(%.4f)" % _.maprad if _.maprad else ""                         ,
      "shear(%.2f)" % _.shear                                               ,
      ""])
             
    for i in range(len(_.points)):
      gls.append(
        "%s = %.3f, %.3f" % (chr(65+i), _.points[i].x, _.points[i].y)
        )

    gls.append(
      "source(%.3f," % _.z_src
    )
    #print "adding points"
    for i in range(len(_.points)):
      if i>0:
        if _.points[i].delay != "":
          delaystr  = ("%.2f" % _.points[i].delay)
        else:
          delaystr = "None"
        delaystr += (")" if i == len(_.points)-1 else ",") #add "," to end of each row,,except last, there add ")"
      else: #this is the first row (which doesnt have a delay to previous)
        delaystr = ""
      
      gls.append(
        "  %s, '%s', %s" % (chr(65+i), _.points[i].type,  delaystr)
      )
      
    #print _.ext_masses
    for em in _.ext_masses:
      gls.append(em.getStr())
      
    gls.extend([
      "model(%s)" % _.n_models                                              ,
      "savestate('%s')" % _.statefilepath                                   ,
      "env().make_ensemble_average()"                                       ,
      "env().arrival_plot(env().ensemble_average, only_contours=True, colors='magenta', clevels=40)"      ,
      "env().overlay_input_points(env().ensemble_average)"      ,
      "pl.gca().axes.get_xaxis().set_visible(False)",
      "pl.gca().axes.get_yaxis().set_visible(False)",
      "pl.savefig('%s%s')" % (_.imgpath, (_.img_name%1))                    ,
      "pl.close()"                                                          ,

      "env().kappa_plot(env().ensemble_average, 0, with_contours=True, clevels=20, vmax=1, with_colorbar=False)",
      "pl.gca().axes.get_xaxis().set_visible(False)",
      "pl.gca().axes.get_yaxis().set_visible(False)",
      "pl.savefig('%s%s')" % (_.imgpath, (_.img_name%2))                    ,
      "pl.close()"                                                          ,

      "env().srcdiff_plot(env().ensemble_average)"                    ,
      "env().overlay_input_points(env().ensemble_average)"      ,
      "pl.gca().axes.get_xaxis().set_visible(False)",
      "pl.gca().axes.get_yaxis().set_visible(False)",
      "pl.savefig('%s%s')" % (_.imgpath, (_.img_name%3))                    ,
      "pl.close()"                                                          ,

      "env().srcdiff_plot_adv(env().ensemble_average, night=True, upsample=8)"      ,
      "env().overlay_input_points(env().ensemble_average)"      ,
      "pl.savefig('%s%s', facecolor='black', edgecolor='none')" % (_.imgpath, ('img%i_ipol.png'%3))    ,
      "pl.close()"                                                          ,
    ])
    
    # append LMT data object
    gls.extend([
      "LMT={",
#      " 'svgViewport' : %i,"     % _.svgViewportSize,
#      " 'orgImgSize'  : %i,"     % _.orgImgSize,
#      " 'pxScale'     : %.5f,"   % _.pxScale,
#      " 'orgPxScale'  : %.5f,"   % _.orgPxScale,
#      " 'gls_version' : '%s',"   % settings.GLS_VERSION ,
#      " 'lmt_version' : '%s',"   % settings.LMT_VERSION ,
      "}"
    ])
 
    
    _.gls = '\n'.join(gls)
    
    #print "saving config"
    
    if not os.path.exists(_.cfg_path):
      #print "create path"
      os.makedirs(_.cfg_path)
    
    f = open(_.cfg_path + _.cfg_file, 'w')
    f.write(_.gls)
    f.close()
    
    #return _.gls


  
#  def createModellingResult(self):
#    #print "createMR easj"
#
#    mr = ModellingResult(
#      lens_data_obj = self.lens_data_obj,
#      json_str      = self.jsonStr,
#      is_final_result = self.is_final)
#    
#    #mr.created_by = self.user_obj
#    mr.created_by_str = self.user_str
#    #mr.log_text = self.logfilename = "bla.log"
#    mr.is_rendered = False
# 
#    mr.hubbletime = self.hubbletime
#    mr.redshift_lens = self.z_lens
#    mr.pixrad = self.pixrad
#    mr.steepness_min = self.steep_min
#    mr.steepness_max = self.steep_max
#    mr.smooth_val = self.smooth_val
#    mr.smooth_include_central = (self.smooth_ic == "True")
#    mr.local_gradient = self.loc_grad
#    mr.is_symm = self.isSym
#    mr.maprad = self.maprad
#    mr.shear = self.shear
#    mr.redshift_source = self.z_src
#    mr.n_models = self.n_models
#
#    mr.n_images = len(self.points)
#    mr.n_sources = 1
#    
#    mr.save()
#    
#    self.result = mr
#    self.result_id = mr.id
#
#    

  def getDict(self):
      
# rafik2018
#      self._.source = []
#      
#      self._.source.append(self._.z_src)
#      for i, pnt in enumerate(self._.points):
#          self._.source.extend(pnt.toGLSLst(i))

      source = []
      
      source.append(self._.z_src)
      for i, pnt in enumerate(self._.points):
          source.extend(pnt.toGLSLst(i))
      
      self._.source = source

          
      #print "in eval (source):", self._.source

      points = []
      for pnt in self._.points:
          points.append(pnt.toDict())
      self._.points = points

      
      self._.jsonObj = ""
      
      #print "in eval (source2:", self._.source
      #print dict(self._)['source']

      exms = []
      for exm in self._.ext_masses:
          exms.append(exm.toDict())

      if len(self._.ext_masses) >0:
          self._.include_priors.append('external_mass')
      
      
      d = dict(self._) #TODO this forgets about the source, check why!!!
      d['source'] = source
      d['ext_masses'] = exms
      d['include_priors'] = self._.include_priors
      
      return d