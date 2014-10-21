# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""


from fabric.api import *
from fabric.utils import *
from fabric.contrib.console import confirm
from pprint import pprint



@task(default=True)
def deploy_server():
    print "instll"
    _check_or_create_dirs()
    _install_pip()
    pass


@task()
def deploy_worker():
    pass



def _check_or_create_dirs():
    
    dirs = [
        env.code_dir,
        
    ]
    
    pprint(env)
    
    puts("cocd with %s"%env.foo)

    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            if run("mkdir -p %s" % code_dir).failed:
                print "using sudo to create dir!"                
                sudo("mkdir -p %s" % code_dir)


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
        
        
        
        
