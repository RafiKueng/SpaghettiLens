from fabric.api import env


class Elem(object):
  
  def __init__(self, name, desc, default):
    self.val = None
    
    self.name = name
    self.desc = desc
    self.dflt = default
    
  def __str__(self):
    if self.val == None:
      raise BaseException("the config option %s was not defined" % self.name)
    return str(self.val)
  
  
  

class ConfigDict(object):
  def __init__(self, init=None):
    if init is not None:
      self.__dict__.update(init)
   
  def __getitem__(self, key):
    return self.__dict__[key]
   
  def __setitem__(self, key, value):
    if type(value)==str:
      try:
        self.__dict__[key].value = value
      except KeyError:
        raise KeyError("No valid configuration option")
    else:
      desc, default = value
      self.__dict__[key] = Elem(key, desc, default)
   
  def __delitem__(self, key):
    del self.__dict__[key]
   
  def __contains__(self, key):
    return key in self.__dict__
   
  def __len__(self):
    return len(self.__dict__)
   
  def __repr__(self):
    return repr(self.__dict__)


c=ConfigDict()

c["NAME"] = (
  "a unique name across all your machine to identiy this install",
  socket.gethostname())
c["REPRO_DIR"] = (
  "the location of the REMOTE reprositry, for future updates (full path, ssh user needs rights)",
    env.cwd + "/src/lmt/" if len(env.cwd)>2 else "~/src/lmt")





