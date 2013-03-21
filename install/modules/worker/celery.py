from fabric.api import env
from fabric.operations import put
from fabric.utils import puts

from install.utils import psw_gen

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



def beforeInstallCmds():
  def fnc():
    # add rabbitmq to sources
    puts("echo deb http://www.rabbitmq.com/debian/ testing main >> /etc/apt/sources.list")
    puts("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
    puts("apt-key add rabbitmq-signing-key-public.asc")
    puts("rm rabbitmq-signing-key-public.asc")
    puts("apt-get update")
  
  return (fnc,)


def getPackagesToInstall():
  pkgs = ()
  
  # rabbit mq
  pkgs += ('rabbitmq-server',)
  
  # glass (numpy,scipy, matplotlib prereq)
  pkgs += ("libfreetype6", "libfreetype6-dev",
           "libpng12-dev", "libblas-dev",
           "libblas3gf", "liblapack-dev",
           "libatlas-base-dev", "libatlas-dev",
           "gfortran")
  
  # glass build
  pkgs += ("subversion",)
  
  return pkgs


def getPipPackagesToInstall():
  pip = ("django-celery", "flower")
  pip += ("numpy", "scipy", "matplotlib")
  return pip


def postInstallCmds():
  def fnc():
    #install glass
    puts("cd "+env.INSTALL_DIR)
    puts("svn checkout https://svn.physik.uzh.ch/repos/itp/glass "+env.WORKER_DIR)
    puts("cd "+env.WORKER_DIR)
    puts("make")
    
  return (fnc,)
  


def setup():
  #rabbitmq server
  
  puts("rabbitmqctl add_user %(BROKER_USER)s %(BROKER_PSW)s" % env)
  puts("rabbitmqctl add_vhost %(BROKER_VHOST)s" % env)
  puts('rabbitmqctl set_permissions -p %(BROKER_VHOST)s %(BROKER_USER)s ".*" ".*" ".*"' % env)
 
 
 