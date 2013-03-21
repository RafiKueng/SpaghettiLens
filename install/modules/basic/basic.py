import os, socket

from fabric.api import env
from fabric.utils import puts
import tempfile

env["TEMP"] = tempfile.gettempdir()


def about():
  return "basic / general setup"


def neededVars():
  return (
    ("NAME", "a unique name across all your machine to identiy this install", socket.gethostname()),
    ("REPRO_DIR", "the location of the reprositry, for future updates", os.getcwd()),
  )


def getPackagesToInstall():
  return ("python-setuptools","python-dev","build-essential")


def betweenInstallCmds():
  def fnc():
    puts("easy_install -U virtualenv ")
    puts("virtualenv py_env")
    puts("source py_env/bin/activate")
    
  return (fnc,)
    


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