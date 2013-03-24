from fabric.api import env
import StringIO

from install import *
from install.utils import _r, _s, _p, _l, _fe


conf = env.conf


def about():
  return "production level django server gunicorn"


def neededVars():
  return (
    ("DJANGO_SERVER_LISTEN_IP", "bind django webserver to ip", "0.0.0.0"),
    ("DJANGO_SERVER_PORT", "bind django webserver to port", "8000"),
  )

def installPackages():
  package_install(('libevent-dev',))



def installPipPackages():
  pip_install(('greenlet','gevent','gunicorn'))






def setup():
  _s("mkdir -p %(INSTALL_DIR)s/run" % conf)
  file = _gen_start_script()
  _p(file, "%(INSTALL_DIR)s/run/start_gunicorn.sh" % conf, use_sudo=True)  #local
  _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s/*" % conf)
  _s("chmod -R 744 %(INSTALL_DIR)s/backend/start_gunicorn.sh" % conf)
  
  
  file = _gen_upstart_conf()
  _p(file, "/etc/init/guni-lmt.conf" % conf, use_sudo=True)  #local
  _s("ln -s -f /lib/init/upstart-job /etc/init.d/guni-lmt")
  _s("initctl reload-configuration")
  
  
  
def _gen_start_script():
  scr = '''#!/bin/bash
set -e
LOGFILE=%(INSTALL_DIR)s%(LOG_DIR)s/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
# user/group to run as
USER=%(SYS_USER)s
GROUP=%(SYS_GROUP)s
PORT=%(DJANGO_SERVER_PORT)s
IP=%(DJANGO_SERVER_LISTEN_IP)s
cd %(INSTALL_DIR)s/backend
source %(INSTALL_DIR)s%(VIRTENV_DIR)s/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
touch $LOGFILE
chown $USER:$GROUP $LOGFILE
exec gunicorn -b $IP:$PORT --user=$USER --group=$GROUP --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE -c settings/gunicorn.py lmt.wsgi:application
''' % conf
  return StringIO.StringIO(scr)


def _gen_upstart_conf():
  ups = '''
description "Test Django instance"
start on runlevel [2345]
stop on runlevel [06]
respawn
respawn limit 10 5
exec %(INSTALL_DIR)s/run/start_gunicorn.sh
''' % conf
  return StringIO.StringIO(ups)



def _gen_upstart_conf2():

  ups = """#!/bin/sh

ADDRESS='127.0.0.1'
#PYTHON="/opt/django/bin/python"
#GUNICORN="/opt/django/bin/gunicorn_django"
PROJECTLOC="%(INSTALL_DIR)s"
#MANAGELOC="$PROJECTLOC/manage.py"
#DEFAULT_ARGS="--workers=3 --daemon --bind=$ADDRESS:"
BASE_CMD="%(INSTALL_DIR)s/run/start_gunicorn.sh"

SERVER1_PORT='8200'
SERVER1_PID="$PROJECTLOC/run/$SERVER1_PORT.pid"

start_server () {
  if [ -f $1 ]; then
    #pid exists, check if running
    if [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
       echo "Server already running on ${ADDRESS}:${2}"
       return
    fi
  fi
  cd $PROJECTLOC
  echo "starting ${ADDRESS}:${2}"
  $BASE_CMD$2 --pid=$1
}

stop_server (){
  if [ -f $1 ] && [ "$(ps -p `cat $1` | wc -l)" -gt 1 ]; then
    echo "stopping server ${ADDRESS}:${2}"
    kill -9 `cat $1`
    rm $1
  else 
    if [ -f $1 ]; then
      echo "server ${ADDRESS}:${2} not running"
    else
      echo "No pid file found for server ${ADDRESS}:${2}"
    fi
  fi
}

case "$1" in
'start')
  start_server $SERVER1_PID $SERVER1_PORT 
  ;;
'stop')
  stop_server $SERVER1_PID $SERVER1_PORT
  ;;
'restart')
  stop_server $SERVER1_PID $SERVER1_PORT
  sleep 2
  start_server $SERVER1_PID $SERVER1_PORT
  ;;
*)
  echo "Usage: $0 { start | stop | restart }"
  ;;
esac

exit 0
""" % conf
  return StringIO.StringIO(ups)




















# override default here with os specific from the submodules  
if env.TARGET_OS == "deb":
  pass
else:
  raise BaseException("this module doesn't support the OS chosen")