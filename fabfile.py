from fabric.operations import local
from fabric.context_managers import lcd

from datetime import datetime as dt
import os

import install.install as i

# makes a fresh install, remote or locally
def install():
  i.install()


# updates an existing install
def update_html(install_dir="D:/temp/lmt"):
  version = local("git describe --abbrev=1 --tags", capture=True)
  time_str = dt.now().strftime("%Y%m%d%H%M")
  v_str = version + "-" + time_str
  
  print ">", v_str
  
  js = {
    'name': 'lmt.'+v_str+'.min.js',
    'root': os.path.join(os.path.normpath(install_dir),'static_html','js'),
    }
  js['full'] = os.path.join(js['root'], js['name'])

  css = {
    'name': 'lmt.'+v_str+'.min.css',
    'root': os.path.join(os.path.normpath(install_dir),'static_html','css'),
    }
  css['full'] = os.path.join(css['root'], css['name'])


  src = {
    'js': './static_html/js',
    'css': './static_html/css'
  }

  js_files = [f for f in os.listdir(src['js']) if f.startswith("lmt") and f.endswith(".js") and not f=='lmt.js']
  
  if not os.path.isdir(js['root']):
    os.makedirs(js['root'])
  with open(js['full'], 'w') as outfile:
    with open(os.path.join(src['js'], 'lmt.js')) as infile:
      for line in infile:
          outfile.write(line)
    for fname in js_files:
      with open(os.path.join(src['js'], fname)) as infile:
        for line in infile:
          outfile.write(line)
          

  css_files = [f for f in os.listdir(src['css']) if f.startswith("lmt") and f.endswith(".css") and not f=='lmt.css']
  
  if not os.path.isdir(css['root']):
    os.makedirs(css['root'])
  with open(css['full'], 'w') as outfile:
    with open(os.path.join(src['css'], 'lmt.css')) as infile:
      for line in infile:
          outfile.write(line)
    for fname in css_files:
      with open(os.path.join(src['css'], fname)) as infile:
        for line in infile:
          outfile.write(line)
  






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
