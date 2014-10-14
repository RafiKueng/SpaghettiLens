#!/usr/bin/env python
import os
import sys

import config


#relative to install dir
dirs = {
  'frontend': 'static_html',
  'backend': 'backend',
  'glass': 'glass',
  'db': 'database',
  'tmp': 'tmp_media',
  'docs': 'docs',
  'env': 'python_env'
}

#exceptions
class InstallDirNotEmpty(Exception):
  pass




def createFolders():
  dir = config.installdir
  
  if os.path.exists(dir):
    raise InstallDirNotEmpty("only install in empty dirs, no upgrades")

  os.makedirs(dir)
  

def createVirtualEnv():
  pass


def installPyPackages():
  pass

  


if __name__ == "__main__":
  print config.var
  pass