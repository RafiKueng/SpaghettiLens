#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/app_name.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=root
GROUP=root
PORT=8001
IP=0.0.0.0
cd /srv/lmt/backend
source ../python_env/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -b $IP:$PORT -w $NUM_WORKERS --user=$USER --group=$GROUP --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE -c lmt/gunicorn_settings.py lmt.wsgi:application