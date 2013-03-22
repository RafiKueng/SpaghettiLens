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
  cwd = env.cwd + "/src/lmt/" if len(env.cwd)>2 else "~/src/lmt" 
  return (
    ("NAME", "a unique name across all your machine to identiy this install", socket.gethostname()),
    ("REPRO_DIR", "the location of the REMOTE reprositry, for future updates (full path, ssh user needs rights)", cwd),
  )


def installPackages():
  package_install(["python-setuptools","python-dev","build-essential","python-pip", "git"])


def betweenInstallCmds():
  _s("easy_install -U virtualenv ")
    


def installPipPackages():
  pip_install(["django","django-lazysignup"])


def postInstallCmds():
  
  _r("mkdir -p " + conf['REPRO_DIR'])
  with _cd(conf['REPRO_DIR']):
    _r("git clone -b master https://github.com/RafiKueng/LensTools.git .")
  with _cd(conf['REPRO_DIR']):
    _s("cp backend %(INSTALL_DIR)s/backend")
  



from fabric.api import env

# override default here with os specific from the submodules  
if env.TARGET_OS == "deb":
  from deb.basic import *
if env.TARGET_OS == "osx":
  from osx.basic import *
if env.TARGET_OS == "win":
  from win.basic import *