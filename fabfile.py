from __future__ import with_statement

import install.install as i

# makes a fresh install, remote or locally
def install():
  i.install()


# updates an existing install
def update_local(install_dir="./build"):
  pass







# restarts any server
def restart():
  pass




def test():
  from fabric.contrib.files import exists as fe
  from fabric.contrib.files import cd

  from fabric.api import env as e
  from install.utils import _cd, _fe, _s
  
  conf = {}
  conf['INSTALL_DIR'] =  '/srv/lmt'
  conf['WORKER_DIR'] = '/worker'
  
  with _cd(conf['INSTALL_DIR']):
    print conf['INSTALL_DIR']
    print conf['WORKER_DIR']+"/run_glass"
    print _fe(conf['INSTALL_DIR']+conf['WORKER_DIR']+"/run_glass")
