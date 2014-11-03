# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:11:04 2014

@author: rafik
"""

from copy import deepcopy
from os.path import join
from attrdict import AttrDict

from fabric.api import env, abort, warn
from fabric.contrib.console import confirm
from fabric import colors

_ = AttrDict()

#
# GENERAL SETTINGS
#


_.WORKER_DEV_HOSTS  = ['localhost']
_.WORKER_TEST_HOSTS = ['192.168.100.2']
_.WORKER_PROD_HOSTS = ['taurus.physik.uzh.ch']


_.PYENV_DIR = 'py_env'


_.APPS_BASE_PATH              = 'apps'
_.APPS_SETTINGS_PATH          = 'apps/apps/settings'
_.APPS_BASE_SETTINGS_FILE     = join(_.APPS_SETTINGS_PATH, 'base.py')
_.APPS_MACHINE_SETTINGS_FILE  = join(_.APPS_SETTINGS_PATH, 'machine.py')
_.APPS_SECRET_SETTINGS_FILE   = join(_.APPS_SETTINGS_PATH, 'secrets.py')





# NOT TUE ANYMORE.. I HOPE PORTNUMERSS ECT WORK AS STRINGS AS WELL
# Attention: in the final config file (which is a python file) strings have
# to be escaped!! So use:
# {'key' : '"str"',}

# This will show up in every config
_.django_base_machine_config = {
    'DATABASE'    : {
        'NAME'    : None,
        'HOST'    : None,
        'PORT'    : None,
        },
    'TIME_ZONE'   : 'Europe/Zürich',
    'STATIC_ROOT' : ''
}

_.django_celery_worker_config = deepcopy(_.django_base_machine_config)
_.django_celery_worker_config.update({
    'BROKER':   {
        'HOST' : 'localhost',
        'PORT' : '5672',
        'VHOST': 'spaghetti_broker',
    },
})





#
# ROLE / TASK SPECIFIC SETTINGS
#


_.ROLEDEFS = {'dev':'',}

if len(env.roles)>1: # or len(env.roles)==0:
    abort("More than one role specified, Go slowly, young padawan..")
elif len(env.roles)==0:
    if confirm(colors.yellow("no role selected!\nUse default [dev]? (N to abort)"), default=True):
        env.roles = ['dev']
    else:
        abort("User abort")

if len(env.tasks)>1:
    warn("More than one task specified (or none), Go slowly, young padawan..\nUse fab --list")
    

if len(env.tasks)==1 and len(env.roles)==1:
    
    task = env.tasks[0]
    role = env.roles[0]
    
    # WORKER related tasks
    if task in ['deploy_worker',]:
        
        _.ROLEDEFS = {
            'dev'   : {'hosts': _.WORKER_DEV_HOSTS},
            'test'  : {'hosts': _.WORKER_TEST_HOSTS}  ,      
            'prod'  : {'hosts': _.WORKER_PROD_HOSTS}  ,      
        }
        
        if role == 'dev':
            _.BASE_DIR = '/tmp/app/spaghetti'
            _.BIN_DIR  = '/tmp/app/bin_spaghetti'
            
        elif role in ['test', 'prod']:
            _.BASE_DIR = '/home/ara/rafik/tmp/apps/spaghetti'
            _.BIN_DIR  = '/home/ara/rafik/tmp/local/bin'
            
            

    # SERVER related tasks            
    elif task in ['testtask']:
        
        _.ROLEDEFS = {
            'test'  : [''],
            'prod'  : ['']        
        }
