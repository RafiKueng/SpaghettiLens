from fabric.api import env
import StringIO

from install.utils import _r, _s, _p, _l, _fe


conf = env.conf


def about():
  return "production level django server gunicorn"


def neededVars():
  return (
    ("DJANGO_SERVER_LISTEN_IP", "(internal?) url for redirects to django server", "0.0.0.0"),
    ("DJANGO_SERVER_PORT", "(internal?) port to django server", "8000"),
  )

def installPackages():
  return ('libevent-dev',)



def installPipPackages():
  return ('greenlet','gevent','gunicorn')






def setup():
  file = _gen_start_script()
  _p(file, "%(INSTALL_DIR)s/backend/start_gunicorn.sh" % conf, use_sudo=True)  #local
  _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s/*" % conf)
  _s("chmod -R 744 %(INSTALL_DIR)s/backend/start_gunicorn.sh" % conf)
  
  
  file = _gen_upstart_conf()
  _p(file, "/etc/init/guni-lmt.conf" % conf, use_sudo=True)  #local
  _s("ln -s /lib/init/upstart-job /etc/init.d/guni-lmt")
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
exec %(INSTALL_DIR)s/backend/start_gunicorn.sh
''' % conf
  return StringIO.StringIO(ups)





# override default here with os specific from the submodules  
if env.TARGET_OS == "deb":
  pass
else:
  raise BaseException("this module doesn't support the OS chosen")