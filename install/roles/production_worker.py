from smtplib import LMTP
SUPPORTED_OSES = ("deb")

from fabric.api import env

def osSupported():
  return env.TARGET_OS in SUPPORTED_OSES

if env.TARGET_OS in SUPPORTED_OSES:
  # import the corresponding modules
  from ..modules.worker import celery as worker


def about():
  return "Production level worker that conects to a existing production server"



########################
## THIS SECTION IS NOT YET DONE
## HERE ARE THE ESSENTIAL parts

'''
mkdir -p ~/src
cd ~/src
git clone https://github.com/RafiKueng/LensTools.git lmt
mkdir ~/bin/lmt
cp -R ~/src/lmt/backend ~/bin/lmt/backend

cd ~/bin/lmt
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
tar xvfz virtualenv-X.X.tar.gz
cd virtualenv-X.X
python virtualenv.py py_env


source py_env/bin/activate
pip install django django-celery MySQL-python

if mysql-python fails:
apt-get build-dep python-mysqldb


svn checkout https://svn.physik.uzh.ch/repos/itp/glass worker
cd worker
make
python setup.py build
make
python setup.py build

if make fails:
apt-get install python-numpy python-scipy python-matplotlib swig glpk texlive-latex-extra dvipng

echo backend : Agg > matplotlibrc
'''


# add this script
# ~/bin/lmt/run_worker_glass
#
# hint: ./run_glass -t <NUM_OF_CPUS> .....

'''
#!/bin/sh

# this is run under /lmt/backend

cd ..
mkdir -p tmp_media/$1
wget -P tmp_media/$1 10.0.0.10/result/$1/cfg.gls
pwd
cd worker
./run_glass -t 2 ../tmp_media/$1/cfg.gls
cd ..
scp tmp_media/$1/img1.png lmt@10.0.0.10:/srv/lmt/tmp_media/$1/
scp tmp_media/$1/img2.png lmt@10.0.0.10:/srv/lmt/tmp_media/$1/
scp tmp_media/$1/img3.png lmt@10.0.0.10:/srv/lmt/tmp_media/$1/

scp tmp_media/$1/log.txt lmt@10.0.0.10:/srv/lmt/tmp_media/$1/
scp tmp_media/$1/state.txt lmt@10.0.0.10:/srv/lmt/tmp_media/$1/

rm tmp_media/$1/state.txt
'''


# get lmt/backend/settings/machine.py and secrets.py from server
# to ~/bin/lmt/backend/settings/
'''
cd ~/bin/lmt/backend/settings/
scp rafik@10.0.0.10:/srv/lmt/backend/settings/secrets.py .
scp rafik@10.0.0.10:/srv/lmt/backend/settings/machine.py .

'''

# make sure mysql on server allows remote access
# /etc/mysql/my.cnf
# bind ip to 0.0.0.0


# create dir
'''
mkdir ~/bin/lmt/tmp_media
''' 



# to enable automatic upload from worker to server (what you really want, unless you have somekind of shared filesystem)
# exchange the ssh keys
# http://www.kriegisch.at/~adi/docs/unix/ssh_autologin.html

'''
# @worker, as worker user
# generate key if non available
ssh-keygen -t rsa

# upload your publickey to server
scp .ssh/id_rsa.pub lmt@10.0.0.10:~/

# log in to server
ssh lmt@10.0.0.10

# @ server, logged in as user SYS_USER: the user the web server run on
mkdir -p ~/.ssh
cat id_rsa.pub >> .ssh/authorized_keys2
'''


####################
# additionally: seperate configs for different worker in a shared file system (like at uzh)
####################
'''
cd ~/bin/lmt

mkdir _def
kopiere alles von lmt in lmt/_def

mkdir <machine_conf>
cd <machine_conf>
ln -s ../_def/backend backend
ln -s ../_def/woker worker
ln -s ../_def/py_env py_env
# DONT move the _py_env dir, this will not work
# OR create the virtualenv with the --relocatable option
# OR change all the virt env files:
# in py_env: 'find . -print | xargs sed -i 's:/old/path:/new/path:g'
ln -s ../_def/tmp_media tmp_media
cp ../_def/run_worker_glass run_worker_glass

nano run_worker_glass

'''




##################
# how to start a worker
##################
'''
screen
cd ~/bin/lmt/backend
source ../py_env/bin/activate
python manage.py celery worker -c 1 -E

[crtl+a, d] to deattach
'''




####################
# how to update worker
#######################

'''
cd ~/src/lmt/
git pull origin master
cp -fR ~/src/lmt/backend ~/bin/lmt/backend
'''














