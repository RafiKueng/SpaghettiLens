import StringIO

from fabric.api import *
from fabric.operations import put
from fabric.utils import puts

from install import *
from install.utils import psw_gen, _r, _s, _cd, _w, _v, _fe, _p
import StringIO
from socket import socket

conf = env.conf


#################################################################################  


def about():
  return "production level worker distrubution server celery (using rabbitmq)"



def neededVars():
  return (
    ("BROKER_HOST", "host of broker service", "localhost"),
    ("BROKER_PORT", "port of broker service", "5672"),
    ("BROKER_USER", "username for broker service", "lmt"),
    ("BROKER_PSW", "password for broker service", "lmt-broker-pw"),#psw_gen()),
    ("BROKER_VHOST", "virtualhost for broker service", "lmt_vh"),
    ("WORKER_DIR", "directory of worker install (GLASS)", "/worker"),
    ("INSTALL_DIR", "//should be set with the role",""),
    ("CELERY_NODENAME", "name this node","worker"),
    ("CELERY_N_THREADS", "n threads to spawn (concurrency)","3"),
    ("CELERY_TASK_TIMELIMIT", "tasks get canceled after X secs","600"),
    ("CELERY_USER", "user to run cerleyd","lmt"),
    ("CELERY_GROUP", "group for celeryd user","www-lmt"),
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
    if not _fe(conf['INSTALL_DIR']+conf['WORKER_DIR']+"/run_glass"):
      _w("svn checkout https://svn.physik.uzh.ch/repos/itp/glass ."+conf['WORKER_DIR'])
      _w("echo backend : Agg > matplotlibrc")
      _w("echo 'backend : Agg' > %(INSTALL_DIR)s%(WORKER_DIR)s/matplotlibrc")
    with _v('.'+conf['WORKER_DIR']):
      _s("make")
      _s("python setup.py build")
    with _cd('.'+conf['WORKER_DIR']):
      _s("chown -R %(SYS_USER)s:%(SYS_GROUP)s %(INSTALL_DIR)s" % conf)
      _s("chmod -R u+rwx %(INSTALL_DIR)s" % conf)

  


def setup():
  #rabbitmq server
  with settings(warn_only=True):
    _s("rabbitmqctl add_user %(BROKER_USER)s %(BROKER_PSW)s" % conf)
    _s("rabbitmqctl add_vhost %(BROKER_VHOST)s" % conf)
    _s('rabbitmqctl set_permissions -p %(BROKER_VHOST)s %(BROKER_USER)s ".*" ".*" ".*"' % conf)
 
  # celery deamon
  
  file = _gen_default_config()
  _p(file, "/etc/default/celeryd", use_sudo=True)
  
  
  file = _gen_init_d_script()
  _p(file, "/etc/init.d/celeryd", use_sudo=True)
  _s("chmod 777 /etc/init.d/celeryd")
  _s("mkdir -p /var/run/celery/")
  _s("chown lmt:www-lmt /var/run/celery/")
  
 
#################################################################################  




## see here for instructions:
## http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#daemonizing


def _gen_default_config():
  ''' generates the default configuration file in /etc/default/celeryd '''

  cfg = '''#
# Name of nodes to start, here we have a single node
CELERYD_NODES="%(CELERY_NODENAME)s"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

#
BASE_DIR="%(INSTALL_DIR)s"

# Where to chdir at start.
CELERYD_CHDIR="$BASE_DIR/backend"

# Python interpreter from environment.
ENV_PYTHON="$BASE_DIR%(VIRTENV_DIR)s/bin/python"

# How to call "manage.py celeryd_multi"
CELERYD_MULTI="$ENV_PYTHON $CELERYD_CHDIR/manage.py celeryd_multi"

# How to call "manage.py celeryctl"
CELERYCTL="$ENV_PYTHON $CELERYD_CHDIR/manage.py celeryctl"

# Extra arguments to celeryd
CELERYD_OPTS="--time-limit=%(CELERY_TASK_TIMELIMIT)s --concurrency=%(CELERY_N_THREADS)s"
''' % conf

  cfg += '\n# %n will be replaced with the nodename.\n'
  cfg += 'CELERYD_LOG_FILE="' + conf['INSTALL_DIR'] + conf['LOG_DIR'] + '/celery_%n.log"\n'
  cfg += 'CELERYD_PID_FILE="/var/run/celery/%n.pid"\n'

  cfg += '''
# Workers should run as an unprivileged user.
CELERYD_USER="%(CELERY_USER)s"
CELERYD_GROUP="%(CELERY_GROUP)s"

# Name of the projects settings module.
export DJANGO_SETTINGS_MODULE="settings.settings"  
''' % conf

  return StringIO.StringIO(cfg)
  
  
  
def _gen_init_d_script():
  
  scr = '''#!/bin/sh -e
# ============================================
#  celeryd - Starts the Celery worker daemon.
# ============================================
#
# :Usage: /etc/init.d/celeryd {start|stop|force-reload|restart|try-restart|status}
# :Configuration file: /etc/default/celeryd
#
# See http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#generic-init-scripts


### BEGIN INIT INFO
# Provides:          celeryd
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: celery task worker daemon
### END INIT INFO

# some commands work asyncronously, so we'll wait this many seconds
SLEEP_SECONDS=5

DEFAULT_PID_FILE="/var/run/celery/%n.pid"
DEFAULT_LOG_FILE="/var/log/celery/%n.log"
DEFAULT_LOG_LEVEL="INFO"
DEFAULT_NODES="celery"
DEFAULT_CELERYD="-m celery.bin.celeryd_detach"

CELERY_DEFAULTS=${CELERY_DEFAULTS:-"/etc/default/celeryd"}

test -f "$CELERY_DEFAULTS" && . "$CELERY_DEFAULTS"

# Set CELERY_CREATE_DIRS to always create log/pid dirs.
CELERY_CREATE_DIRS=${CELERY_CREATE_DIRS:-0}
CELERY_CREATE_RUNDIR=$CELERY_CREATE_DIRS
CELERY_CREATE_LOGDIR=$CELERY_CREATE_DIRS
if [ -z "$CELERYD_PID_FILE" ]; then
    CELERYD_PID_FILE="$DEFAULT_PID_FILE"
    CELERY_CREATE_RUNDIR=1
fi
if [ -z "$CELERYD_LOG_FILE" ]; then
    CELERYD_LOG_FILE="$DEFAULT_LOG_FILE"
    CELERY_CREATE_LOGDIR=1
fi

CELERYD_LOG_LEVEL=${CELERYD_LOG_LEVEL:-${CELERYD_LOGLEVEL:-$DEFAULT_LOG_LEVEL}}
CELERYD_MULTI=${CELERYD_MULTI:-"celeryd-multi"}
CELERYD=${CELERYD:-$DEFAULT_CELERYD}
CELERYD_NODES=${CELERYD_NODES:-$DEFAULT_NODES}

export CELERY_LOADER

if [ -n "$2" ]; then
    CELERYD_OPTS="$CELERYD_OPTS $2"
fi

CELERYD_LOG_DIR=`dirname $CELERYD_LOG_FILE`
CELERYD_PID_DIR=`dirname $CELERYD_PID_FILE`

# Extra start-stop-daemon options, like user/group.
if [ -n "$CELERYD_USER" ]; then
    DAEMON_OPTS="$DAEMON_OPTS --uid=$CELERYD_USER"
fi
if [ -n "$CELERYD_GROUP" ]; then
    DAEMON_OPTS="$DAEMON_OPTS --gid=$CELERYD_GROUP"
fi

if [ -n "$CELERYD_CHDIR" ]; then
    DAEMON_OPTS="$DAEMON_OPTS --workdir=$CELERYD_CHDIR"
fi


check_dev_null() {
    if [ ! -c /dev/null ]; then
        echo "/dev/null is not a character device!"
        exit 75  # EX_TEMPFAIL
    fi
}


maybe_die() {
    if [ $? -ne 0 ]; then
        echo "Exiting: $* (errno $?)"
        exit 77  # EX_NOPERM
    fi
}

create_default_dir() {
    if [ ! -d "$1" ]; then
        echo "- Creating default directory: '$1'"
        mkdir -p "$1"
        maybe_die "Couldn't create directory $1"
        echo "- Changing permissions of '$1' to 02755"
        chmod 02755 "$1"
        maybe_die "Couldn't change permissions for $1"
        if [ -n "$CELERYD_USER" ]; then
            echo "- Changing owner of '$1' to '$CELERYD_USER'"
            chown "$CELERYD_USER" "$1"
            maybe_die "Couldn't change owner of $1"
        fi
        if [ -n "$CELERYD_GROUP" ]; then
            echo "- Changing group of '$1' to '$CELERYD_GROUP'"
            chgrp "$CELERYD_GROUP" "$1"
            maybe_die "Couldn't change group of $1"
        fi
    fi
}


check_paths() {
    if [ $CELERY_CREATE_LOGDIR -eq 1 ]; then
        create_default_dir "$CELERYD_LOG_DIR"
    fi
    if [ $CELERY_CREATE_RUNDIR -eq 1 ]; then
        create_default_dir "$CELERYD_PID_DIR"
    fi
}

create_paths() {
    create_default_dir "$CELERYD_LOG_DIR"
    create_default_dir "$CELERYD_PID_DIR"
}

export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"


_get_pid_files() {
    [ ! -d "$CELERYD_PID_DIR" ] && return
    echo `ls -1 "$CELERYD_PID_DIR"/*.pid 2> /dev/null`
}

stop_workers () {
    $CELERYD_MULTI stopwait $CELERYD_NODES --pidfile="$CELERYD_PID_FILE"
    sleep $SLEEP_SECONDS
}


start_workers () {
    $CELERYD_MULTI start $CELERYD_NODES $DAEMON_OPTS        \
                         --pidfile="$CELERYD_PID_FILE"      \
                         --logfile="$CELERYD_LOG_FILE"      \
                         --loglevel="$CELERYD_LOG_LEVEL"    \
                         --cmd="$CELERYD"                   \
                         $CELERYD_OPTS
    sleep $SLEEP_SECONDS
}


restart_workers () {
    $CELERYD_MULTI restart $CELERYD_NODES $DAEMON_OPTS      \
                           --pidfile="$CELERYD_PID_FILE"    \
                           --logfile="$CELERYD_LOG_FILE"    \
                           --loglevel="$CELERYD_LOG_LEVEL"  \
                           --cmd="$CELERYD"                 \
                           $CELERYD_OPTS
    sleep $SLEEP_SECONDS
}

check_status () {
    local pid_files=`_get_pid_files`
    [ -z "$pid_files" ] && echo "celeryd is stopped" && exit 1

    local one_failed=
    for pid_file in $pid_files; do
        local node=`basename "$pid_file" .pid`
        local pid=`cat "$pid_file"`
        local cleaned_pid=`echo "$pid" | sed -e 's/[^0-9]//g'`
        if [ -z "$pid" ] || [ "$cleaned_pid" != "$pid" ]; then
            echo "bad pid file ($pid_file)"
        else
            local failed=
            kill -0 $pid 2> /dev/null || failed=true
            if [ "$failed" ]; then
                echo "celeryd (node $node) (pid $pid) is stopped, but pid file exists!"
                one_failed=true
            else
                echo "celeryd (node $node) (pid $pid) is running..."
            fi
        fi
    done

    [ "$one_failed" ] && exit 1 || exit 0
}


case "$1" in
    start)
        check_dev_null
        check_paths
        start_workers
    ;;

    stop)
        check_dev_null
        check_paths
        stop_workers
    ;;

    reload|force-reload)
        echo "Use restart"
    ;;

    status)
        check_status
    ;;

    restart)
        check_dev_null
        check_paths
        restart_workers
    ;;
    try-restart)
        check_dev_null
        check_paths
        restart_workers
    ;;
    create-paths)
        check_dev_null
        create_paths
    ;;
    check-paths)
        check_dev_null
        check_paths
    ;;
    *)
        echo "Usage: /etc/init.d/celeryd {start|stop|restart|kill|create-paths}"
        exit 64  # EX_USAGE
    ;;
esac

exit 0'''
  
  return StringIO.StringIO(scr)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

