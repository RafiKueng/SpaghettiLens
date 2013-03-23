import os

from fabric.api import local, settings, abort, run, cd, env, sudo
from fabric.utils import puts
from fabric.operations import prompt
from fabric.contrib.console import confirm
from package import *
from virtualenv import *
from utils import _r, _s, _cd


from importlib import import_module
import pkgutil

import roles as roles_mod



SKIP_PREPARE = True
SKIP_PKGS = True
SKIP_BETW = True
SKIP_PIP = True
SKIP_POST = True


def install():
  env.conf = {}
  config = env.conf 

  puts("\nSelect target os")
  config['TARGET_OS'] = prompt("[deb]ian/ubuntu, [win]dows, [osx]; default:", key="TARGET_OS", default="deb")
  
  puts("What kind of install do you wanna do?")

  path = os.path.dirname(roles_mod.__file__)
  roles = [name for _, name, x in pkgutil.iter_modules([path])]
  forbidden = ()
  for i, role in enumerate(roles):
    module = import_module("install.roles."+role)
    if module.osSupported():
      puts("[" + str(i)+"] " + module.about())
    else:
      puts("[" + str(i)+"] " + "NOT SUPPORTED ON THIS OS")
      forbidden += (str(i),)
  #print "[" + str(i+1)+"] " + "select my own modules to isntall"
  
  def valchoice(ch):
    #print ch
    if ch in forbidden: raise KeyError("This option is not supported on the chosen os")
    try:
      ch = int(ch)
      #if ch==5: return "_own_modules"
      return roles[ch]
    except:
      raise KeyError("please choose a number from the list")
    
  config['ROLE'] = prompt("Choose number", key="ROLE", default=0, validate=valchoice)
  print roles
  
  
  if env.ROLE =="_own_modules":
    raise BaseException("onw modules not implemented")
    #module.database = import_module("install.modules."+mod)
  else:
    module = import_module("install.roles."+env.ROLE)
    
  select_config()
    
  mod = module.__dict__["basic"]
  iCmd = mod.getInstallCommand()
    
  modules = [('basic', module.__dict__["basic"]),
             ('role', module),
             ('database', module.__dict__["database"]),
             ('djangoserver', module.__dict__["djangoserver"]),
             ('staticserver', module.__dict__["staticserver"]),
             ('worker', module.__dict__["worker"])]
  
  puts("\nYou chose the following modules to install:")
  for i, (name, mod) in enumerate(modules):
    try:
      puts("* " + name+": " + mod.about())
    except:
      pass
    
  puts("\nGetting the needed information:")
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      vars = mod.neededVars()
      for var in vars:
        #print var[0], var[1], var[2]
        try:
          # do we arleady know this parameter?
          puts("--- " + var[0] + " already set to: " + config[var[0]])
        except KeyError:
          config[var[0]] = prompt("--- "+var[0] + " ("+var[1]+")", key=var[0], default=var[2])
    except AttributeError:
      puts("--- no needed vars")
      pass      
  puts("Done, got all information\n")
  
  save_config()
  
  
  puts("\nInstalling the packages:")
  
  install_cmds_pre = []
  install_pkgs = []
  install_cmd_between = []
  install_pips = []
  install_cmds_after = []
  
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      install_cmds_pre += [mod.beforeInstallCmds]
      puts("--- pre packages cmds")
    except AttributeError:
      pass
    
    try:
      install_pkgs += [mod.installPackages]
      puts("--- packages to install")
    except AttributeError:
      pass
    
    try:
      install_cmd_between += [mod.betweenInstallCmds]
      puts("--- between install cmds")
    except AttributeError:
      pass
    
    try:
      install_pips += [mod.installPipPackages]
      puts("--- pip packages")
    except AttributeError:
      pass
    
    try:
      install_cmds_after += [mod.postInstallCmds]
      puts("--- post pip cmds")
    except AttributeError:
      pass


  if not SKIP_PREPARE:  
    puts("\n= preparing packages")
    for cmd in install_cmds_pre:
      puts("________")
      cmd()

  if not SKIP_PKGS:  
    puts("\n= installing binary packages")
    _s("apt-get update")
    for cmd in install_pkgs:
      puts("________")
      cmd()
    package_install_start()
    
  if not SKIP_BETW:
    puts("= between pkgs and pip install commands")
    for cmd in install_cmd_between:
      puts("________")
      cmd()
    
  if not SKIP_PIP:
    puts("\n= installing pip packages")
    for cmd in install_pips:
      puts("________")
      cmd()
    pip_install_start()

  if not SKIP_POST:
    puts("\n= after pip install commands")
    for cmd in install_cmds_after:
      puts("________")
      cmd()  

  puts("Done, all packages installed\n")



  puts("\nTesting the installs:")
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      mod.testInstall()
    except AttributeError:
      puts("--- no need to test anything")
  puts("Done, everything tested\n")
  

  
  puts("\nSetup the software:")
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      mod.setup()
    except AttributeError as e:
      puts(str(e))
      #raise
      puts("--- no need to setup anything")
  puts("Done, everything setup\n")


  puts("\nTest the final setup:")
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      mod.testSetup()
    except AttributeError:
      puts("--- no need to test anything")
    
  puts("all tests OK\n")
  
  print config
  





def save_config():
  pass

def select_config():
  pass
