import os, string, random

import fabric.api
from fabric.api import *
from contextlib import contextmanager as _contextmanager

from virtualenv import virtenv

FAB_DEBUG = False

if FAB_DEBUG:
  # rerout run comands for debugging
  _r = lambda *s: puts("RUN  | " + " ".join(s))
  _s = lambda *s: puts("SUDO | " + " ".join(s))
  _w = lambda *s: puts("WWW  | " + " ".join(s))
  _p = lambda *s, **ss: puts("PUT  | " + " ".join(s))
  _l = lambda  s: puts("LOCPY| " + s)
  _L = lambda  s: puts("LOC  | " + s)
  
  def _fe(*s):
    puts("FILE EXISTS? | " + " ".join(s))
    return False
  
  @_contextmanager
  def _v(dir="./"):
    puts("VENV / " + dir)
    yield
    puts("     \---")
    
  @_contextmanager
  def _cd(dir="./"):
    puts("CD   / " + dir)
    yield
    puts("     \---")

else:
  _r = fabric.api.run
  _s = fabric.api.sudo
  def _w(s): fabric.api.sudo(s, user=fabric.api.env.conf['SYS_USER'])
  _p = fabric.api.put
  def _l(s): exec s
  _L = fabric.api.local
  _v = virtenv
  
  _fe = fabric.contrib.files.exists
  _cd = fabric.context_managers.cd



def path(*args):
  path = os.path.join(*args)
  return os.path.normcase(path)


def psw_gen(size=8, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for x in range(size))



      

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
