# -*- coding: utf-8 -*-
"""

note the use of lambda functions that get evauated if needed
(so default values could be changed on the fly, and depending values change..)

definitions:
- dir: single folder
- path full path
- URL = HOST + RESSLOC + FILE


Created on Fri Oct 17 14:11:04 2014

@author: rafik
"""

from copy import deepcopy
from os.path import join
from attrdict import AttrDict

from fabric.api import env, abort, warn
from fabric.contrib.console import confirm
from fabric import colors

from fab_tools import *

_ = AttrDict()

#
# GENERAL SETTINGS
#


_.WORKER_DEV_HOSTS  = ['localhost']
_.WORKER_TEST_HOSTS = ['192.168.100.2']
_.WORKER_PROD_HOSTS = ['taurus.physik.uzh.ch']


_.PYENV_DIR                     = 'py_env'

_.TMPDIR                        = 'ttemp'
_.TMPPATH_                      = lambda: join(_.ROOT_PATH, _.TMPDIR)




_.ROOT_PATH                     = '/data/labs.spacewarps.org'
_.HOST                          = 'labs.spacewarps.org'




_.HTDOCS_DIR                    = 'htdocs'
_.HTDOCS_PATH_                  = lambda: join(_.ROOT_PATH, _.HTDOCS_DIR)


'''
_.                              = ''
_.                              = ''
_.                              = ''
_.                              = ''
_.                              = ''
'''

# where is stuff in the dev repro
_.SRC                           = AttrDict()
_.SRC.DJANGODIR                 = 'apps'
_.SRC.HTMLDIR                   = 'html'
_.SRC.TEMPLATES                 = 'deploy/files'
_.SRC.PIP_REQ_FILE              = 'pip_requirements_worker.txt'
_.SRC.PIP_REQ_RPATH_            = lambda: join(_.SRC.TEMPLATES, _.SRC.PIP_REQ_FILE)


_.APPS                          = AttrDict()
_.APPS.DIR                      = 'django_app'                                  # the root of the django project (manage.py is in here)
_.APPS.PATH_                    = lambda: join(_.ROOT_PATH, _.APPS.DIR)
_.APPS.PROJECTNAME              = 'apps'                                        # the name of the django project

#_.APPS.SETTINGS                 = AttrDict()
_.APPS.SETTINGS_RPATH_          = lambda: join(_.APPS.DIR, _.APPS.PROJECTNAME)
_.APPS.SETTINGS_BASE_           = lambda: join(_.APPS.SETTINGS_RPATH_(), 'base.py')
_.APPS.SETTINGS_MACHINE_        = lambda: join(_.APPS.SETTINGS_RPATH_(), 'machine.py')
_.APPS.SETTINGS_SECRETS_        = lambda: join(_.APPS.SETTINGS_RPATH_(), 'secrets.py')
_.APPS.SETTINGS_VERSION_        = lambda: join(_.APPS.SETTINGS_RPATH_(), 'version.py')

_.APPS.MEDIA_DIR                = 'tmp_media'

#
#_.APPS_BASE_PATH              = 'apps'
#_.APPS_SETTINGS_PATH          = 'apps/apps/settings'
#_.APPS_BASE_SETTINGS_FILE     = join(_.APPS_SETTINGS_PATH, 'base.py')
#_.APPS_MACHINE_SETTINGS_FILE  = join(_.APPS_SETTINGS_PATH, 'machine.py')
#_.APPS_SECRET_SETTINGS_FILE   = join(_.APPS_SETTINGS_PATH, 'secrets.py')

_.EXTAPPS                       = AttrDict()
_.EXTAPPS.DIR                   = 'ext_apps'

_.SPAGHETTI                     = AttrDict()
_.SPAGHETTI.HTMLFILES_DIR       = 'spaghetti'
_.SPAGHETTI.HTMLFILES_PATH_     = lambda: join(_.HTDOCS_PATH_(), _.SPAGHETTI.HTMLFILES_DIR)

_.SPAGHETTI.RESSLOC             = 'spaghetti'                                   # the part in the url...
_.SPAGHETTI.URL_                = lambda: _.HOST + _.SPAGHETTI.RESSLOC

_.GLASS                         = AttrDict()
_.GLASS.TMPBUILDDIR             = 'tmp_glass'
_.GLASS.REPROURL                = 'https://github.com/RafiKueng/glass.git'
_.GLASS.COMMIT                  = '7d8413280b'


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
    warnn("no role selected!")
    if confirm("Use default [dev]? (N to abort)", default=True):
        env.roles = ['dev']
    else:
        abort("User abort")

if len(env.tasks)>1:
    abort("More than one task specified (or none), Go slowly, young padawan..\nUse fab --list")
    

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
            _.ROOT_PATH = '/tmp/app/swlabs_worker'
            _.BIN_DIR   = '/tmp/app/swlabs_worker_bin'
            
            _.TMPDIR    = 'worker_tmp'
            
        elif role in ['test', 'prod']:
            _.ROOT_PATH = '/home/ara/rafik/tmp/apps/swlabs_worker'
            _.BIN_DIR   = '/home/ara/rafik/tmp/local/bin'
            
            

    # SERVER related tasks            
    elif task in ['testtask']:
        
        _.ROLEDEFS = {
            'test'  : [''],
            'prod'  : ['']        
        }


#
# WRITE DOWN THE ACTUAL CONFIG
#

def config_r(_):
    for k, v in _.items():
        if isinstance(v, AttrDict):
            v = config_r(v)

        else:
            #new =  AttrDict()
            if k.endswith('_'):
                k = k[:-1]
                try:
                    v = v()
                except TypeError:
                    pass

        #new[k] = v
        _[k] = v
        #print k, v
    return _
    
    

settings = config_r(_)



