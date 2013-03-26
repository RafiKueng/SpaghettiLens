from __future__ import with_statement

import os

import fabric.api
import fabric.colors

from fabric.api import *

from contextlib import contextmanager as _contextmanager

import utils

fabric.api.env['PIP'] = []
 
 
def virtualenv_create(dir='/srv/active/',site_packages=True):
  pass


@_contextmanager
def virtenv(dir=''):
  """runs a command inside the virtual env"""
  # http://stackoverflow.com/questions/1180411/activate-a-virtualenv-via-fabric-as-deploy-user
  
  
  if dir =='':
    #env.directory = '/path/to/virtualenvs/project'
    dir = env.conf['INSTALL_DIR']
    
  env.dir = dir
    
  env.activate = 'source '+env.conf['INSTALL_DIR']+env.conf['VIRTENV_DIR']+'/bin/activate'
  
  with cd(env.dir):
    with prefix(env.activate):
      yield



def pip_install(list):
  if type(list)==str: list = [list]
  fabric.api.env['PIP'].extend(list)

def pip_install_start():
  """ Runs pip install """
  list = fabric.api.env['PIP']
  
  with utils._v():
    #utils._s('pip install -i http://f.pypi.python.org/simple %s'%(' '.join(list)))
    utils._s('pip install %s'%(' '.join(list)))