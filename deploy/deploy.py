# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""


from fabric.api import *
from fabric.utils import *
from fabric.contrib.console import confirm
from pprint import pprint
import datetime as dt
import os

def runc(s):
    return run(s, capture=True)


@task(default=True)
def deploy_server():
    print "instll"
    _check_or_create_dirs()
    _install_pip()
    pass


@task()
def deploy_worker():
    
    '''    
    mkdir -p /home/ara/rafik/src/SpaghettiLens && cd /home/ara/rafik/src/SpaghettiLens

    tag = v1.6.3
    mkdir $tag && cd $tag
    git clone --branch v1.6.3 --depth 1 https://github.com/RafiKueng/SpaghettiLens.git .

    oder besser:
    
    git clone --branch master --depth 1 https://github.com/RafiKueng/SpaghettiLens.git .
    git fetch --tags
    tag = git describe --abbrev=1 --tags --match 'v*'
    glsversion = git describe --abbrev=0 --tags --match "gls\.v[0-9]*
    time_str = dt.now().strftime("%Y%m%d%H%M")
    v_str = version + "-" + time_str
    
    
    '''
    
    src_dir  = '/home/ara/rafik/tmp/src/spaghettilens' #TODO don't use remote src folder!
    inst_dir = '/home/ara/rafik/tmp/apps/spaghettilens'
    bin_dir  = '/home/ara/rafik/tmp/local/bin'
    
    pyenv_dir = 'py_env'
    
    _check_or_create_dirs([src_dir, inst_dir, bin_dir])

    if exists(src_dir + '/.git'):
        with cd(src_dir):
            run('git pull origin master')
    else:
        with cd(src_dir):
            run('git clone --branch master --depth 1 https://github.com/RafiKueng/SpaghettiLens.git .')

    with cd(src_dir):
        run('git fetch --tags', capture=True)
        lmt_version = runc('git describe --abbrev=6 --tags --match "lmt\.v[0-9]*"')
        gls_version = runc('git describe --abbrev=0 --tags --match "gls\.v[0-9]*"')
        
        t = lmt_version.split('-')
        if len(t)==3:
            version, ahead, hashstr = t
        else:
            version = t
            ahead = ""
            hashstr = ""
        major, minor, revis = version[1:].split('.')
        
        dt.now().strftime("%Y%m%d%H%M")
        
        lmt_version = (int(major), int(minor), int(revis), int(ahead), hashstr, timestamp)
        gls_version = int(gls_version[5:])
        

    #get glass
    #TODO


    # copy files:
    dirlist = ['backend']
    
    
    # setup virtualenv
    with cd(src_dir):
        pydir = os.path.join(src_dir, pyenv_dir)
        
        if not exists(pydir, 'bin/activate'):
            run('virtualenv $s' % pyenv_dir)
            
            with prefix('source %s' % (os.path.join(pyenv_dir, 'bin/activate'))):
                run('pip install -r deploy/requirements.txt')
                

    # create startup scripts
    
        








def _check_or_create_dirs(dirs=None):
    
    if dirs==None:
        dirs = [
            env.code_dir,
        ]
    
    pprint(env)
    
    puts("cocd with %s"%env.foo)

    with settings(warn_only=True):
        for d in dirs:
            if run("test -d %s" % d).failed:
                if run("mkdir -p %s" % d).failed:
                    print "using sudo to create dir!"                
                    sudo("mkdir -p %s" % d)
                    sudo("chmod 777 -r %s" % s) #TODO test this line
                    #sudo("chown %s %s" % (user, d)) #TODO test this line


def _install_pip():
    with cd(code_dir):
        pass
    
    
def _init_or_update_git():

    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        #run("touch app.wsgi")
        
        
        
        
