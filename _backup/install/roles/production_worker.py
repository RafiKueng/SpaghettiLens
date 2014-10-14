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
cp -R ~/src/lmt/backend ~/bin/lmt/

cd ~/bin/lmt
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
tar xvfz virtualenv-X.X.tar.gz
cd virtualenv-X.X
python virtualenv.py py_env


source py_env/bin/activate
pip install django django-celery MySQL-python fabric flower ipython

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
# how to update worker - backend
#######################

'''
cd ~/src/lmt/
git pull origin master
cp -fR ~/src/lmt/backend ~/bin/lmt/backend
'''


####################
# how to update worker - glass
#######################

'''

'''





######################
# how to bootstrap python properly
######################

'''
# install python to local dir
mkdir ~/local
cd local 
mkdir src
cd src
wget http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz
tar zxfv Python-2.7.5.tgz
cd Python-2.7.5
./configure --prefix=$HOME/local
make -j2
make install
# check if right python, else add ~/local/bin to path
where python

# add commonly used modules
cd ~/local/src
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python2.7
curl --silent --show-error --retry 5 https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7
pip install virtualenv
pip install virtualenvwrapper
pip install numpy
pip install yolk
pip install scipy matplotlib

pip install ipython[zmq,qtconsole,notebook,test]


'''





################################
# new instal // UP TO DATE
# tailored for uzh systems


'''

# get the soruces

mkdir -p ~/src
cd ~/src

git clone https://github.com/RafiKueng/LensTools.git lmt
cd lmt
git checkout master
# or
git pull origin master --tags

# create bin structre
mkdir ~/bin/lmt
cd ~/bin/lmt

# if multiple configs, use this:
mkdir _default # i don't like hidden dirs..
mkdir dualcore_conf
mkdir quadcore_conf

# get the data
cp -R ~/src/lmt/backend ~/bin/lmt/_default


# create python env (assume local custom python in ~/bin/python27, with virtualenv installed)
cd ~/bin/lmt/_default
virtualenv py_env  --system-site-packages

# get additional packages
pip install django django-celery MySQL-python fabric south django-lazysignup









# # create python env (assume local custom python in ~/bin/python27, see above)
# cd ~/lmt/_default
# curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
# tar xvfz virtualenv-X.X.tar.gz
# cd virtualenv-X.X
# ~/bin/python27/bin/python setup.py build
# ~/bin/python27/bin/python setup.py install
# cd ..
# rm -r virtual*
# 
# ~/bin/python27/bin/virtualenv py_env --python=/home/kurs/rafik/bin/python27/bin/python
# 
# source py_env/bin/activate
# 
# pip install numpy  # on university machines, make sure to have libblas-devel, libatlas-devel ect.. ask doug
# pip install scipy matplotlib
# pip install django django-celery MySQL-python fabric #flower ipython



# get the worker / glass
cd ~/bin/lmt/_default
svn checkout https://svn.physik.uzh.ch/repos/itp/glass worker

cp -aif ~/src/lmt/glass/. ~/bin/lmt/_default/worker # update glass with SL changes.. we'd really like to have a own glass repro...

cd worker
make
python setup.py build
make

# if make fails:
# apt-get install swig glpk texlive-latex-extra dvipng

echo backend : Agg > matplotlibrc



mkdir tmp_media

cd ~/bin/lmt
~/bin/lmt% ln -s _default/backend dual/backend
~/bin/lmt% ln -s _default/backend quad/backend
~/bin/lmt% ln -s _default/worker dual/worker
~/bin/lmt% ln -s _default/worker quad/worker
~/bin/lmt% ln -s _default/tmp_media quad/tmp_media
~/bin/lmt% ln -s _default/tmp_media dual/tmp_media



# setup the starter file
cd ~/bin/lmt/_default
echo
#------------
#!/bin/sh

# this is run under /lmt/backend

cd ..
mkdir -p tmp_media/$1
wget -P tmp_media/$1 mite/result/$1/cfg.gls
#pwd
cd worker
./run_glass -t 2 ../tmp_media/$1/cfg.gls
cd ..
scp tmp_media/$1/* lmt@mite:/srv/lmt/tmp_media/$1/

#scp tmp_media/$1/img1.png lmt@mite:/srv/lmt/tmp_media/$1/
#scp tmp_media/$1/img2.png lmt@mite:/srv/lmt/tmp_media/$1/
#scp tmp_media/$1/img3.png lmt@mite:/srv/lmt/tmp_media/$1/

#scp tmp_media/$1/log.txt lmt@mite:/srv/lmt/tmp_media/$1/
#scp tmp_media/$1/state.txt lmt@mite:/srv/lmt/tmp_media/$1/

rm tmp_media/$1/*
#------------
> run_worker_glass

chmod +x run_worker_glass



# get the proper settings files

cd ~/bin/lmt/_default/backend/settings/
scp rafik@10.0.0.10:/srv/lmt/backend/settings/secrets.py .
scp rafik@10.0.0.10:/srv/lmt/backend/settings/machine.py .


change machine.py accordingly!!!
database_host and broker_host

'''

