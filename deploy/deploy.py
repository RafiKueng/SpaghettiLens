# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""


from fabric.api import *
from fabric.utils import *
from fabric import operations as ops

from fabric import colors

from fabric.contrib import console, files, project

#from fabric.contrib.console import confirm
#from fabric.contrib.files import *
#from fabric.contrib.project import *
#from fabric.colors import *

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
    
    
    curr_branch = local("git symbolic-ref --short -q HEAD", capture=True)

    if curr_branch != 'master':
        warn(colors.yellow("""
You're not on the master branch (but on `%s`), but you try to update the live workers.
Thats probably not what you want to do...
Check commit your changes and merge with master, then test, then update the worker nodes."""%curr_branch))
        if not console.confirm("Continue anyways?", default=False):
            abort("Aborted due to wrong local branch")
        
        
    
    #src_dir  = '/home/ara/rafik/tmp/src/spaghettilens'
    inst_dir = '/home/ara/rafik/tmp/apps/spaghettilens'
    bin_dir  = '/home/ara/rafik/tmp/local/bin'
    
    pyenv_dir = 'py_env'
    
    _check_or_create_dirs([inst_dir, bin_dir])

#    with cd(src_dir):
#        if exists(src_dir + '/.git'):
#            run('git pull origin master')
#        else:
#            run('git clone --branch master --depth 1 https://github.com/RafiKueng/SpaghettiLens.git .')

    local('git fetch --tags')
    #lmt_version = run('git describe --abbrev=6 --tags --match "lmt\.v[0-9]*"')
    lmt_version = localc('git describe --abbrev=6 --tags --match "v[0-9]*"') #TODO delete this once switched to new naming schema
    gls_version = localc('git describe --abbrev=0 --tags --match "gls\.v[0-9]*"')
    
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
    
    version_str = '%s__%s__%s.%s.%s_%s' % (timestamp, hashstr, major, minor, revis, ahead)
    
    #pprint(lmt_version)
    #pprint(gls_version)
        
    rinst_dir = os.path.join(inst_dir, version_str) #'real' install dir
    _check_or_create_dirs([rinst_dir])

    dirlist = [
        'backend',
        'tmp_media',
        'deploy',
    ]
    paths_to_copy = [
        'backend',
        'deploy/pip_requirements_worker.txt'
    ]


    with cd(rinst_dir):
        
        full_dirlist = [os.path.join(rinst_dir, d) for d in dirlist]
        _check_or_create_dirs(full_dirlist)
        
        for loc in paths_to_copy:
            #project.rsync_project(local_dir=loc, remote_dir=rinst_dir, exclude='.git')
            put(local_path=loc, remote_path=loc)
        
        # setup python, pip and virtualenv
        # assumption: we have  python, but nothing else
        # solution: create a local python (~~/.local/bin)
        # which is used to create a virtualenv
        
        #http://forcecarrier.wordpress.com/2013/07/26/installing-pip-virutalenv-in-sudo-free-way/

        with settings(warn_only=True):
            if run('python --version').failed:
                abort('No python available remote... aborting')
            if run('pip -V').failed:
                warn('no pip found remote. getting and installing a remote version into ~/.local/bin')
                run('curl -O https://bootstrap.pypa.io/get-pip.py')
                run('python get-pip.py --user')
                warn(colors.yellow('Make sure the local pip is on path "~/.local/bin" (~/.bashrc)'))
                if not console.confirm('Finished putting it on path?'):
                    abort('then do it now!!')

        run('pip install --user virtualenv')
        
        run('virtualenv %s' %pyenv_dir)
        
        with prefix('source %s' % os.path.join(pyenv_dir, 'bin/activate')):
            run('pip install -r deploy/pip_requirements_worker.txt')
            
    
    with cd(inst_dir):
        if files.exists('_current'):
            run('rm _current')
        run('ln -s %s _current' % version_str)
    
    
    
    
    # setup virtualenv
#    with cd(src_dir):
#
#        pydir = os.path.join(src_dir, pyenv_dir)
#            
#        if not exists(os.path.join(pydir, 'bin/activate'), is_file=True):
#            run('virtualenv $s' % pyenv_dir)
#            
#            with prefix('source %s' % (os.path.join(pyenv_dir, 'bin/activate'))):
#                run('pip install -r deploy/requirements.txt')
                

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
        
        
        
        
