from __future__ import with_statement

from fabric.api import env, warn, settings, get, put
from fabric.colors import *

from install.utils import _r, _s, _p, _l, _L, _fe, _cd, _w
import install.utils as utils
from StringIO import StringIO
from fabric.utils import puts


SUPPORTED_OSES = ("deb")
conf = env.conf

def osSupported():
  return env.TARGET_OS in SUPPORTED_OSES

if env.TARGET_OS in SUPPORTED_OSES:
  # import the corresponding modules
  from ..modules.basic import basic as basic 
  from ..modules.database import mysql as database 
  from ..modules.django import gunicorn as djangoserver
  from ..modules.static import nginx as staticserver
  from ..modules.worker import celery as worker


def about():
  return "production setup, uses production level servers, minifies code ect..."


def neededVars():
  return (
    ("REMOTE_IP", "machine to install", "10.0.0.10"),
    ("INSTALL_DIR", "where to install the server (absolute path)", "/srv/lmt"),
    ("VIRTENV_DIR", "where to install virtualenv (relative)", "/py_env"),
    ("SYS_USER", "the username the whole stuff will be running on (will be created)", "lmt"),
    ("SYS_PSW", "the password for SYS_USER (if user exists the pw IWLL BE CHANGED)", 'pw' ),#utils.psw_gen()),
    ("SYS_GROUP", "the group of the sys_user", "www-lmt"),
    ("LOG_DIR", "Directory for all log files (relative)", "/logs"),
    ("GIT_BRANCH", "which branch to use (take master)", "deploy")
    
  )


def beforeInstallCmds():
  
  # add users and groups
  with settings(warn_only=True):
    _s("groupadd -f %(SYS_GROUP)s" % conf)
    res = _s('adduser --ingroup %(SYS_GROUP)s --disabled-password --gecos "" %(SYS_USER)s' % conf)
    if res.return_code==4:
      warn(yellow("user already exists"))
    _s('echo "%(SYS_USER)s:%(SYS_PSW)s" | chpasswd' % conf)
    #exchange ssh jeys to automate login
    env.password = conf['SYS_PSW']
    _L("ssh-copy-id -i ~/.ssh/id_dsa.pub %(SYS_USER)s@%(REMOTE_IP)s")


def betweenInstallCmds():
  _s("mkdir -p %(INSTALL_DIR)s" % conf)
  _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s" % conf)
  _s("chmod u+rwx %(INSTALL_DIR)s" % conf)
  
  with _cd(conf['INSTALL_DIR']):
    if not _fe(conf['INSTALL_DIR']+conf['VIRTENV_DIR']):
      _w("virtualenv --distribute --system-site-packages .%(VIRTENV_DIR)s" % conf)
    pass
  
def postInstallCmds():
  
  _s("mkdir -p " + conf['REPRO_DIR'])
  with _cd(conf['REPRO_DIR']):
    if _fe('.git'):
      _s("git reset --hard HEAD" % conf)
      _s("git checkout %(GIT_BRANCH)s" % conf)
      _s("git pull origin %(GIT_BRANCH)s" % conf)
    else:
      _s("git clone -b %(GIT_BRANCH)s https://github.com/RafiKueng/LensTools.git ." % conf)
  
  #log files go here
  _s("mkdir -p %(INSTALL_DIR)s%(LOG_DIR)s" % conf)
  _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s%(LOG_DIR)s" % conf)
  _s("chmod -R 744 %(INSTALL_DIR)s%(LOG_DIR)s" % conf)  

    

    
#################################################################################  



def setup():
  
  # BACKEND
  
  _s("cp -f -r %(REPRO_DIR)s/backend %(INSTALL_DIR)s/" % conf)
    
  _create_django_settings()
  _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s/*" % conf)
  _s("chmod -R 777 *" % conf)
  
  # STATIC HTML STUFF
  #with _cd(conf['REPRO_DIR']):
  #  _s("cp -f -R backend %(INSTALL_DIR)s/backend" % conf)
    




def finish():

  #set rights
  _s("find %(INSTALL_DIR)s -type d -print0 | xargs -0 chmod 755" % conf) 
  _s("find %(INSTALL_DIR)s -type f -print0 | xargs -0 chmod 644" % conf)
  _s("find %(INSTALL_DIR)s/run -type f -print0 | xargs -0 chmod 744" % conf)
  _s("find %(INSTALL_DIR)s%(VIRTENV_DIR)s -type f -print0 | xargs -0 chmod 744" % conf)
  _s("chmod u+x %(INSTALL_DIR)s%(WORKER_DIR)s/run_glass")



#################################################################################  

def _create_django_settings():

  inp = StringIO()
  with settings(user=conf['SYS_USER'], password=conf['SYS_PSW']):
    get(conf['INSTALL_DIR']+'/backend/settings/machine.template.py', inp)
  outp = StringIO(inp.getvalue() % conf)
  put(outp, conf['INSTALL_DIR']+'/backend/settings/machine.py', use_sudo=True)
  
  inp = StringIO()
  with settings(user=conf['SYS_USER'], password=conf['SYS_PSW']):
    get(conf['INSTALL_DIR']+'/backend/settings/secrets.template.py', inp)
  outp = StringIO(inp.getvalue() % conf)
  put(outp, conf['INSTALL_DIR']+'/backend/settings/secrets.py', use_sudo=True)
    
  
  
  
  
  
  
  
  