import os

from fabric.api import local, settings, abort, run, cd, env, sudo
from fabric.utils import puts
from fabric.operations import prompt
from fabric.contrib.console import confirm

from importlib import import_module
import pkgutil

import roles as roles_mod

def install():
  config = {}

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
  
  
  if env.ROLE =="_own_modules":
    raise BaseException("onw modules not implemented")
    #module.database = import_module("install.modules."+mod)
  else:
    module = import_module("install.roles."+env.ROLE)
    
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
          tmp=config[var[0]]
        except KeyError:
          config[var[0]] = prompt("--- "+var[0] + " ("+var[1]+")", key=var[0], default=var[2])
    except AttributeError:
      puts("--- no needed vars")
      pass      
  puts("Done, got all information\n")
  
  
  puts("\nInstalling the packages:")
  
  install_cmds_pre = ()
  install_pkgs = ()
  install_cmd_between = ()
  install_pips = ()
  install_cmds_after = ()
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      install_cmds_pre += mod.beforeInstallCmds()
    except AttributeError:
      puts("--- no pre packages to install here")
    
    try:
      install_pkgs += mod.getPackagesToInstall()
    except AttributeError:
      puts("--- no packages to install here")
    
    try:
      install_cmd_between += mod.betweenInstallCmds()
    except AttributeError:
      puts("--- no between package install commands here")
    
    try:
      install_pips += mod.getPipPackagesToInstall()
    except AttributeError:
      puts("--- no pip packages install to install here")
    
    try:
      install_cmds_after += mod.postInstallCmds()
    except AttributeError:
      puts("--- no post pip install commands here")
      
  puts("= preparing packages")
  for cmd in install_cmds_pre:
    #TODO: execute command
    puts(cmd)
  
  puts("= installing binary packages")
  if len(install_pkgs) > 0:
    #TODO: execute command
    #puts('apt-get install ' + ' '.join(pkgs))
    puts(iCmd(install_pkgs))
    
  puts("= between pkgs and pip install commands")
  for cmd in install_cmd_between:
    #TODO: execute command
    puts(cmd)
    
  puts("= installing pip packages")
  if len(install_pips) > 0:
    #TODO: execute command
    #puts('apt-get install ' + ' '.join(pkgs))
    puts("pip install "+" ".join(install_pips))

  puts("= after pip install commands")
  for cmd in install_cmds_after:
    #TODO: execute command
    puts(cmd)  

  puts("Done, all packages installed\n")


  puts("\nTesting the installs:")
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      mod.testInstall()
    except AttributeError:
      puts("--- no need to install anything")
  puts("Done, everything tested\n")
  
  
  puts("\nSetup the software:")
  for i, (name, mod) in enumerate(modules):
    puts("* "+name)
    try:
      mod.setup()
    except AttributeError:
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
  
  
