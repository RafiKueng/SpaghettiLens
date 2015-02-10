# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:43:52 2014

@author: rafik
"""
from __future__ import absolute_import

import os

from fabric import api
from fabric import colors
from fabric.contrib import console, files

from .settings import settings as _S


class GetOutOfLoop( Exception ):
    pass


def localc(s):
    return api.local(s, capture=True)


def lvenv(c):
    '''executes a command using venv locally'''
    venv = 'source %s' % os.path.join(_S.SRC.PYENV_DIR, 'bin', 'activate')
    return api.local(venv + ' && '+c,shell='/bin/bash')
    
def lmanagepy(c):
    '''locally executes a command for manage.py using venv'''
    cds = 'cd %s && ./manage.py ' % _S.SRC.DJANGODIR
    return lvenv(cds + c)


def rvenv(c, warn_only=False, quiet=False):
    '''executes a command using venv remotely'''
    venv = 'source %s' % os.path.join(_S.PYENV_DIR, 'bin', 'activate')
    return api.run(venv + ' && '+c, shell='/bin/bash', warn_only=warn_only, quiet=quiet)
    

#def exists(path, is_dir=False, is_file=False):
#    with settings(warn_only=True):
#        if is_dir:
#            return run("test -d %s" % path).succeeded
#        elif is_file:
#            return run("test -f %s" % path).succeeded
#        else:
#            return run("test -e %s" % path).succeeded

def inform(s):
    api.puts(colors.green('\n> '+s+'\n'+'-'*80), show_prefix=False)
    

def warnn(s):
    api.warn(colors.yellow('\n> '+s))
    

def debugmsg(s):
    api.puts(colors.red('DEBUG> '+s), show_prefix=False)

def confirm(s, default=True):
    return console.confirm(colors.yellow('\n> '+s), default)
        
def errorr(s):
    api.puts(colors.red('\n> '+s))
    
def choose(s, opts, list_options=False):
    '''choose one char out of given options

    choose('[R]etry, [Q]uit', 'rq')
    the first one is the default value
    doesn't care about upper/lower space, returns chosen option in lower case
    '''
    #optslow = [_.lower() for _ in opts]
    #val = lambda s: s.lower() in optslow
    val = '^[%s]$' % '|'.join(opts.lower() + opts.upper())    
    if list_options:
        lo=' [%s]' % '|'.join(opts)
    else:
        lo=''
    return api.prompt(colors.magenta(s + lo), default=opts[0].upper(), validate=val).lower()
    
        
    

def check_or_create_dirs(dirs=None):
    for d in dirs:
        api.run("mkdir -p %s" % d)




def install_pkg(pkgs):

    pkgnames = []
    
    for pkg in pkgs:
        
        if pkg.requ:
            api.sudo("zypper -n in %s" % " ".join(pkg.requ))

        if pkg.file:
            lnk = '/'.join((_S.PKG.PREFIX,) + pkg.path + (pkg.file,)) + pkg.ext
            fname = pkg.file + pkg.ext
            pkgnames.append(fname)
            if not files.exists(fname):
                api.run("wget %s" % lnk)
    
    if pkgnames:
        c = api.sudo("rpm -Uihv %s" % " ".join(pkgnames), warn_only=True)
        if c.failed:
            warnn('There was an error. Check the log!')
            api.promt('Any key to continue, ctrl-c to abort')
