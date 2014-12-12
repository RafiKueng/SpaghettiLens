# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:02:18 2014

@author: rafik
"""
from __future__ import absolute_import



from fabric.api import settings, local, task
#from fabric.utils import *

#from fabric import operations as ops
#from fabric.contrib import console, files, project


from .fab_tools import GetOutOfLoop
from .fab_tools import inform, warnn, errorr, confirm, choose
from .fab_tools import lmanagepy

from .settings import settings as _S

#import unittest as ut
from . import test_cases as tcs

#import os


@task
def utest():
    '''runs the Django unittests'''
    
    warnn('starting django unittests in endless loop')
    
    while True:
        inform("STARTING DJANGO UNITTESTS")
        with settings(warn_only=True):
            rc = lmanagepy('test -v 2 --failfast')

        if not rc.failed:
            inform("RUN SUCCESSFUL FINISHED - QUITTING")
            break

        if not confirm('Another run?'):
            errorr('ABORTING')
            break
    


@task
def static_analysis():
    '''runs the static code analysis tools on selected files
    
    prospector is used, make sure to pip install it
    '''
    
    dirs = [
        _S.SRC.DJANGODIR,
        _S.SRC.DEPLOYDIR,
    ]
    
    files   = [
        './fabfile.py',
        './deploy/test_tasks.py',
    ]
    
    paths = dirs + files
    
    try:
        inform("STARTING STATIC CODE ANALYSIS")
        for p in paths:
            while True:
                inform("- checking %s" % p)
                with settings(warn_only=True):
                    rc = local('prospector %s' % p)
                
                if rc.failed:
                    txt = 'Rcq'
                    c = choose('[%s]erun current test, [%s]ontinue, [%s]uit' % tuple(txt), ''.join(sorted(txt)))
                    if c=='c':
                        break
                    elif c=='q':
                        raise GetOutOfLoop
                else:
                    inform("- successful, continuing")
                    break
                

#        if not confirm('Another run?', default=False):
#            raise GetOutOfLoop

        inform("STATIC CODE ANALYSIS FINISHED")

    except GetOutOfLoop:
        errorr('abort')


@task
def testtt():
    print choose('choose from', 'ynr')


@task
def test_serversetup():
    
    tcs.runTestSuite_ServerAll()
















