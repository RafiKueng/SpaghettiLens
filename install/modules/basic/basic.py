from __future__ import with_statement

import os, socket

from fabric.api import env
from fabric.utils import puts
import tempfile

from install import * 
from install.utils import _r, _s


env["TEMP"] = tempfile.gettempdir()


def about():
  return "basic / general setup"


def neededVars():
  return (
    ("NAME",
     "a unique name across all your machine to identiy this install",
     socket.gethostname()),
    ("REPRO_DIR",
     "the location of the REMOTE reprositry, for future updates (full path, ssh user needs rights)",
     env.cwd + "/src/lmt/" if len(env.cwd)>2 else "~/src/lmt"),
    ("TIMEZONE",
     "the name of the timezone the server is in",
     "Europe/Zurich"),
    ("SECRET_KEY",
     "Secret key for django app",
     psw_gen(size=32))
    )


def installPackages():
  package_install(["python-setuptools","python-dev","build-essential","python-pip", "git"])


def betweenInstallCmds():
  _s("easy_install -U virtualenv ")
    


def installPipPackages():
  pip_install(["django","django-lazysignup"])


def postInstallCmds():
  pass
  



from fabric.api import env

# override default here with os specific from the submodules  
if env.TARGET_OS == "deb":
  from deb.basic import *
if env.TARGET_OS == "osx":
  from osx.basic import *
if env.TARGET_OS == "win":
  from win.basic import *