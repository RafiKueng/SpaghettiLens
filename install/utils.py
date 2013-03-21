import os, string, random

import fabric.api
from fabric.api import *
from contextlib import contextmanager as _contextmanager


def path(*args):
  path = os.path.join(*args)
  return os.path.normcase(path)


def psw_gen(size=8, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for x in range(size))



env.directory = '/path/to/virtualenvs/project'
env.activate = 'source /path/to/virtualenvs/project/bin/activate'

@_contextmanager
def virtenv():
  """runs a command inside the virtual env"""
  # http://stackoverflow.com/questions/1180411/activate-a-virtualenv-via-fabric-as-deploy-user
  with cd(env.directory):
    with prefix(env.activate):
      yield
      

def isLocal():
  if fabric.api.env.host=="" and len(fabric.api.env.hosts)==0:
    return True
  else:
    return False
  
  
  
  
def run_py(str):
  """
  Runs a command either locally or remote, if hosts are set
  """
  if type(str)=="str":
    str=[str]
  
  if isLocal():
    for cmd in str:
      exec(cmd)
  else:
    for i, cmd in enumerate(str):
      if cmd.startswith("return "):
        str[i] = cmd.replace("return", "print", 1)
    return fabric.api.run('python -c "' + '; '.join(str) + '"')
  
  

def detect_os():
  if 'conf' in fabric.api.env and 'OS' in fabric.api.env.conf:
    return fabric.api.env.conf['OS']
  if isLocal():
    import platform
    outp = platform.uname()
  else:
    outp = fabric.api.run('python -c "import platform; print platform.uname()"') + ""

  print "outp:", outp
  type = eval(outp)[0]
  if type=="Windows":
    type="win"
    distr=""
    ver=eval(outp)[2]
  if type=="Linux":
    type="linux"
    outp = fabric.api.run('python -c "import platform; print platform.linux_distribution()"')
    distr, verno, ver = eval(outp)

  # ('win', '', '7')
  # ('linux', 'Ubuntu', 'precise')
  os = (type, distr, ver)
  if not 'conf' in fabric.api.env:
    fabric.api.env['conf'] = {}
  fabric.api.env.conf['OS'] = os
  return os
