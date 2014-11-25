# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:02:18 2014

@author: rafik
"""


from fabric.api import *
from fabric.utils import *

from fabric import operations as ops
from fabric import colors
from fabric.contrib import console, files, project


from fab_tools import *

from settings import settings as _S

#import unittest 

import test_cases as tcs

import os


@task
def utest():
    '''runs the Django unittests'''
    
    warnn('starting django unittests in endless loop')
    
    while True:
        inform("STARTING DJANGO UNITTESTS")
        with settings(warn_only=True):
            lmanagepy('test -v 2 --failfast')
        inform("RUN FINISHED")
        if not console.confirm('\nAnother run?'):
            warn('abort')
            break
    


@task
def static_analysis():
    
    dirs = [
        _S.SRC.DJANGODIR,
        _S.SRC.DEPLOYDIR,
    ]
    
    files   = [
        './fabfile.py',
        './tests.py',            
    ]
    
    for d in dirs:
        local('prospector %s' % d)
    for f in files:
        os.system('prospector -0 %s' % f)

