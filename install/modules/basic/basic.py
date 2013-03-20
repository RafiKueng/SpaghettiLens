import os, socket

from fabric.api import env
from fabric.utils import puts



def about():
  return "basic / general setup"


def neededVars():
  return (
    ("NAME", "a unique name across all your machine to identiy this install", socket.gethostname()),
    ("REPRO_DIR", "the location of the reprositry, for future updates", os.getcwd()),
  )

  

def betweenInstallCmds():
  return ("virtualenv py_env","source py_env/bin/activate")


def getPipPackagesToInstall():
  return ("django","django-lazysignup")

  

from fabric.api import env

# override default here with os specific from the submodules  
if env.TARGET_OS == "deb":
  from deb.basic import *
if env.TARGET_OS == "osx":
  from osx.basic import *
if env.TARGET_OS == "win":
  from win.basic import *