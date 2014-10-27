# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""


from fabric.api import *
from fabric.utils import *
from fabric.contrib.console import confirm
from fabric.colors import *

from fab_tools import *

from pprint import pprint
from datetime import datetime as dt
import os







@task(default=True)
def deploy_server():
    print "instll"
    _check_or_create_dirs([env.code_dir,])
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
    
    curr_branch = local("git symbolic-ref --short -q HEAD", capture=True)

    if curr_branch != 'master':
        warn(yellow("""
You're not on the master branch (but on `%s`), but you try to update the live workers.
Thats probably not what you want to do...
Check commit your changes and merge with master, then test, then update the worker nodes."""%curr_branch))
        if not confirm("Continue anyways?", default=False):
            abort("Aborted due to wrong local branch")
        
        
    
    #src_dir  = '/home/ara/rafik/tmp/src/spaghettilens' #TODO don't use remote src folder!
    inst_dir = '/home/ara/rafik/tmp/apps/spaghettilens'
    bin_dir  = '/home/ara/rafik/tmp/local/bin'
    
    pyenv_dir = 'py_env'
    
    _check_or_create_dirs([inst_dir, bin_dir])

    with cd(src_dir):
        if exists(src_dir + '/.git'):
            run('git pull origin master')
        else:
            run('git clone --branch master --depth 1 https://github.com/RafiKueng/SpaghettiLens.git .')

    with cd(src_dir):
        run('git fetch --tags')
        #lmt_version = run('git describe --abbrev=6 --tags --match "lmt\.v[0-9]*"')
        lmt_version = run('git describe --abbrev=6 --tags --match "v[0-9]*"') #TODO delete this once switched to new naming schema
        gls_version = run('git describe --abbrev=0 --tags --match "gls\.v[0-9]*"')
        
        t = lmt_version.split('-')
        if len(t)==3:
            version, ahead, hashstr = t
        else:
            version = t[0]
            ahead = "0"
            hashstr = ""
        major, minor, revis = version[1:].split('.')
        
        timestamp = dt.now().strftime("%Y%m%d%H%M")
        
        lmt_version = (int(major), int(minor), int(revis), int(ahead), hashstr, timestamp)
        gls_version = int(gls_version[5:])
        
        pprint(lmt_version)
        pprint(gls_version)
        

    #get glass
    #TODO


    # copy files:
    dirlist = ['backend', 'tmp_media']
    
    # which dirs and files to copy from src to inst_dir
    paths_to_copy = ['backend']

    full_dirlist = [inst_dir + d for d in dirlist]

    _check_or_create_dirs(full_dirlist)
    
    for p in paths_to_copy:
        pass

    
    
    # setup virtualenv
    with cd(src_dir):

        pydir = os.path.join(src_dir, pyenv_dir)
            
        if not exists(os.path.join(pydir, 'bin/activate'), is_file=True):
            run('virtualenv $s' % pyenv_dir)
            
            with prefix('source %s' % (os.path.join(pyenv_dir, 'bin/activate'))):
                run('pip install -r deploy/requirements.txt')
                

    # create startup scripts
    
        








def _check_or_create_dirs(dirs=None):
    
    
    #pprint(env)
    
    #puts("cocd with %s"%env.foo)

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
        
        
        
        
