from fabric.api import *
from fabric.operations import put
from fabric.utils import puts

from install import *
from install.utils import psw_gen, _r, _s, _cd, _w, _v

conf = env.conf


#################################################################################  


def about():
  return "production level worker distrubution server celery (using rabbitmq)"



def neededVars():
  return (
    ("BROKER_USER", "username for broker service", "lmt"),
    ("BROKER_PSW", "password for broker service", psw_gen()),
    ("BROKER_VHOST", "virtualhost for broker service", "lmt_vh"),
    ("WORKER_DIR", "directory of worker install (GLASS)", "/worker"),
    ("INSTALL_DIR", "//should be set with the role","")
  )


#################################################################################  


def beforeInstallCmds():
  # add rabbitmq to sources
  v = {'file': "/etc/apt/sources.list",
       'txt': "deb http://www.rabbitmq.com/debian/ testing main"}
  _s("grep -q '%(txt)s' %(file)s || echo '%(txt)s' >> %(file)s" % v)
  _r("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
  _s("apt-key add rabbitmq-signing-key-public.asc")
  _r("rm rabbitmq-signing-key-public.asc")

  


def installPackages():
  pkgs = ()
  
  # rabbit mq
  pkgs += ('rabbitmq-server',)
  
  # glass (numpy,scipy, matplotlib prereq)
  pkgs += ("python-numpy", "python-scipy", "python-matplotlib", "swig", "glpk", "texlive-latex-extra", "dvipng")
  # don't build yourself, and put it to virtualenv.. it's a pain in the ...
  # texlive extra is needed because matplotlib uses fonts not available in the base install.. might have changed by now
  
  # glass build
  pkgs += ("subversion",)

  package_install(pkgs)


def installPipPackages():
  piplist = ("django-celery", "flower")
  #piplist += ("numpy", "scipy", "matplotlib")
  pip_install(piplist)


def postInstallCmds():
  with _cd(conf['INSTALL_DIR']):
    _w("svn checkout https://svn.physik.uzh.ch/repos/itp/glass ."+conf['WORKER_DIR'])
    _w("echo backend : Agg > matplotlibrc")
    with _v('.'+conf['WORKER_DIR']):
      _s("make")
      _s("python setup.py build")
    with _cd('.'+conf['WORKER_DIR']):
      _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s" % conf)
      _s("chmod -R u+rwx %(INSTALL_DIR)s" % conf)

  


def setup():
  #rabbitmq server
  
  _s("rabbitmqctl add_user %(BROKER_USER)s %(BROKER_PSW)s" % conf)
  _s("rabbitmqctl add_vhost %(BROKER_VHOST)s" % conf)
  _s('rabbitmqctl set_permissions -p %(BROKER_VHOST)s %(BROKER_USER)s ".*" ".*" ".*"' % conf)
 
 
#################################################################################  


