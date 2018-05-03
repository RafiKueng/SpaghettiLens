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
from datetime import datetime as dt
from attrdict import AttrDict

from fabric.api import env, abort#, abort, warn
#from fabric.contrib.console import confirm

#from fab_tools import abort

_ = AttrDict()

env.TIMESTAMP = dt.now().strftime("%Y%m%d%H%M")

#
# GENERAL SETTINGS
#


_.WORKER_DEV_HOSTS  = ['localhost']
_.WORKER_TEST_HOSTS = ['192.168.100.10']
_.WORKER_PROD_HOSTS = ['taurus.physik.uzh.ch']

_.SERVER_TEST_HOST  = ['192.168.100.10']
_.SERVER_PROD_HOST  = ['root@swlabs.physik.uzh.ch']

# where is the server located
# used for worker to connect to
# will be overwritten below in role specific part
_.SERVERHOST = "127.0.0.1" 


#
# which packages to install
#
# get the link from https://software.opensuse.org
#
# name: basic backage name
# requ: requirements to install first (using zypper)
# path: which package exactly (the url to the file)
# file: the complete filename (as reported by rpm -q <name>, and also part of the url)
# ext : the extension (.rpm)

_.PKG                           = AttrDict()

_.PKG.OSVER                     = 'openSUSE_Leap_42.1'
_.PKG.ARCH                      = 'x86_64'
_.PKG.PREFIX                    = "http://download.opensuse.org/repositories"

# https://software.opensuse.org/package/couchdb
_.PKG.COUCH                     = [
    AttrDict({
        'name': 'couchdb',
        'requ': ('libmozjs185-1_0', 'libopenssl-devel'),
        'path': ('server:', 'database', 'openSUSE_13.2',_.PKG.ARCH),
        'file': 'couchdb-1.6.1-56.3.x86_64',
        'ext' : '.rpm'
    })]

# https://software.opensuse.org/package/erlang
# https://software.opensuse.org/package/erlang-epmd
_.PKG.ERLANG                    = [
    AttrDict({
        'name': 'erlang',
        'requ': ('unixODBC',),
        'path': ('openSUSE:','Leap:','42.1:','Update','standard',_.PKG.ARCH),
        'file': 'erlang-18.0.3-8.1.x86_64',
        'ext' : '.rpm'
    }),
    AttrDict({
        'name': 'erlang-epmd',
        'requ': (),
        'path': ('openSUSE:','Leap:','42.1:','Update/standard',_.PKG.ARCH),
        'file': 'erlang-epmd-18.0.3-8.1.x86_64',
        'ext' : '.rpm'
    })]

# https://software.opensuse.org/package/rabbitmq-server
# http://download.opensuse.org/repositories/openSUSE:/13.1/standard/x86_64/rabbitmq-server-3.1.5-2.2.2.x86_64.rpm
# https://software.opensuse.org/package/rabbitmq-server-plugins
# http://download.opensuse.org/repositories/openSUSE:/13.1/standard/x86_64/rabbitmq-server-plugins-3.1.5-2.2.2.x86_64.rpm
_.PKG.RABBITMQ                  = [
    AttrDict({
        'name': 'rabbitmq-server',
        'requ': (),
        'path': ('openSUSE:/Leap:/42.1','standard', _.PKG.ARCH),
        'file': 'rabbitmq-server-3.5.1-2.7.x86_64',
        'ext' : '.rpm'
    }),
    AttrDict({
        'name': 'rabbitmq-server-plugins',
        'requ': (),
        'path': ('openSUSE:/Leap:/42.1', 'standard', _.PKG.ARCH),
        'file': 'rabbitmq-server-plugins-3.5.1-2.7.x86_64',
        'ext' : '.rpm'
    }),
    ]

#
# use apache from zypper
#
_.PKG.APACHE = [
    AttrDict({
        'name': 'apache',
        'requ': ('apache2', 'apache2-mod_wsgi'),
        'path': (),
        'file': '',
        'ext' : ''
    }),
]

#
# use texlive from zypper
#
_.PKG.TEXLIVE = [
    AttrDict({
        'name': 'texlive',
        'requ': ('texlive-scheme-medium',),
        'path': (),
        'file': '',
        'ext' : ''
    }),
]



#
# python is around. but there might be some requrements needed for some packages
#
_.PKG.PYTHON = [
    AttrDict({
        'name': 'python-imaging',
        'requ': (
            'libjpeg62-devel','libtiff-devel',   # for pillow
            ),
        'path': (),
        'file': '',
        'ext' : ''
    }),
]




_.PYENV_DIR                     = 'py_env'

_.TMPDIR                        = 'ttemp'
_.TMPPATH_                      = lambda: join(_.ROOT_PATH, _.TMPDIR)

# is set per task / role
#_.BIN_PATH                     = lambda: join(_.ROOT_PATH, 'bin')


# for server
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
#_.SRC.HTMLDIR                   = 'html'
#_.SRC.PYENV_DIR                 = 'py_env'
_.SRC.DEPLOYDIR                 = 'deploy'
_.SRC.TEMPLATES                 = 'deploy/files'
_.SRC.PIP_REQ_FILE              = 'pip_requirements.txt'                        # filename on remote machine
_.SRC.PIP_REQ_FILE_WRK          = 'pip_requirements_worker.txt'
#_.SRC.PIP_REQ_RPATH_WRK_        = lambda: join(_.SRC.TEMPLATES, _.SRC.PIP_REQ_FILE_WRK)
_.SRC.PIP_REQ_FILE_SRV          = 'pip_requirements_server.txt'
#_.SRC.PIP_REQ_RPATH_SRV_        = lambda: join(_.SRC.TEMPLATES, _.SRC.PIP_REQ_FILE_SRV)


# SETTINGS FOR DJANGO APPS  # TODO remove this and replace all by the _.DJANGO
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



# FOLDER FOR EXTERNAL APPS
_.EXTAPPS                       = AttrDict()
_.EXTAPPS.DIR                   = 'ext_apps'


#SETTING UP EXTERNAL APPS
_.GLASS                         = AttrDict()
_.GLASS.TMPBUILDDIR             = 'tmp_glass'
_.GLASS.REPROURL                = 'https://github.com/RafiKueng/glass.git'
_.GLASS.COMMIT                  = '02d2969' #'0e3cc108ae' #'1f1f3527' #'8c3dd2c' #'64b2be69'




_.SPAGHETTI                     = AttrDict()
_.SPAGHETTI.HTMLFILES_DIR       = 'spaghetti'
_.SPAGHETTI.HTMLFILES_PATH_     = lambda: join(_.HTDOCS_PATH_(), _.SPAGHETTI.HTMLFILES_DIR)

_.SPAGHETTI.RESSLOC             = 'spaghetti'                                   # the part in the url...
_.SPAGHETTI.URL_                = lambda: _.HOST + _.SPAGHETTI.RESSLOC


# SERVER SERVICES CONFIG
_.SVCCONFIG                     = AttrDict()
_.SVCCONFIG.DIR                 = 'config'  # dir in root 
_.SVCCONFIG.PATH_               = lambda: join(_.ROOT_PATH, _.SVCCONFIG.DIR) # dir in root 

# SERVER SERVICES DATA
_.SVCDATA                       = AttrDict()
_.SVCDATA.DIR                   = 'data'  # dir in root 
_.SVCDATA.PATH_                 = lambda: join(_.ROOT_PATH, _.SVCDATA.DIR) # dir in root 


# SERVER SERVICES CONFIGURATIONS

_.RABBITMQ                      = AttrDict()
_.RABBITMQ.USER                 = 'rabbituser' #TODO change these values...
_.RABBITMQ.PASSWORD             = 'rabbitpsw'
_.RABBITMQ.VHOST                = 'swlabs'
_.RABBITMQ.PORT                 = 5672
_.RABBITMQ.GUESTPSW             = 'guest1'


_.COUCHDB                       = AttrDict()
_.COUCHDB.CONF_NAME             = 'couchdb_swlabs.ini' # name on target server system
_.COUCHDB.CONF_TMPL             = 'couchdb_swlabs.ini' # name of template in local repro
_.COUCHDB.ORGCONF_DIR           = '/etc/couchdb/local.d' # here comes the symlink
_.COUCHDB.ORGCONF_PATH_         = lambda: join(_.COUCHDB.ORGCONF_DIR, _.COUCHDB.CONF_NAME)
_.COUCHDB.CONF_PATH_            = lambda: join(_.SVCCONFIG.PATH_(), _.COUCHDB.CONF_NAME)

_.COUCHDB.DATA_DIR              = 'couchdb_data'
_.COUCHDB.DATA_PATH_            = lambda: join(_.SVCDATA.PATH_(), _.COUCHDB.DATA_DIR)

_.COUCHDB.ADDRESS               = '127.0.0.1'
_.COUCHDB.PORT                  = 5984
_.COUCHDB.AUTH                  = "{couch_httpd_auth, default_authentication_handler}"




_.APACHE                        = AttrDict()
_.APACHE.CONF_NAME              = 'apache_swlabs.conf' # filename on server
_.APACHE.CONF_TMPL              = 'apache_swlabs.conf' # filename in repro

_.APACHE.ORGCONF_DIR            = '/etc/apache2/vhosts.d'
_.APACHE.ORGCONF_PATH_         = lambda: join(_.APACHE.ORGCONF_DIR, _.APACHE.CONF_NAME)
_.APACHE.CONF_PATH_            = lambda: join(_.SVCCONFIG.PATH_(), _.APACHE.CONF_NAME)


_.DJANGOAPP                     = AttrDict()
_.DJANGOAPP.SRCDIR              = _.SRC.DJANGODIR    # how is the folder with the django project named in the repro
#_.DJANGOAPP.SRCPATH_            = _.SRC.DJANGODIR
_.DJANGOAPP.ROOT_DIR            = 'django_apps' # the name of the root django project on remote, eg the folder name on the server, doesn't depend on local dir (thats SRC_DIR)
_.DJANGOAPP.CONF_TMPL           = 'django_machine_settings.py' # the name of the template in the repro
_.DJANGOAPP.CONF_NAME           = 'machine_settings.py' # the name of the final config file on srv
_.DJANGOAPP.PROJ_DIR            = '_app'    # the main folder / project name (where settings.py and wsgi.py are) local and remote
_.DJANGOAPP.LINK_DIR_           = lambda: join(_.DJANGOAPP.ROOT_DIR, _.DJANGOAPP.PROJ_DIR)

_.DJANGOAPP.SETTINGS            = AttrDict()
das = _.DJANGOAPP.SETTINGS
das.STATICFOLDER                = 'static'
das.STATICURL                   = '/static'
das.MEDIAFOLDER                 = 'media'
das.MEDIAURL                    = '/media'

_.DJANGOAPP.REQ_FOLDERS         = [das.STATICFOLDER, das.MEDIAFOLDER]



#
# stuff for the worker
#
_.CELERY                        = AttrDict()
_.CELERY.STARTSCRIPT_TMPL       = 'start_celery' # the filename in tmpl folder in repro
_.CELERY.STARTSCRIPT_NAME       = 'start_celery' # the name on the worker (inside _.BIN_PATH)
# this is for the server
_.CELERY.FLOWERSTARTSCRIPT_TMPL = 'start_flower' # the filename in tmpl folder in repro
_.CELERY.FLOWERSTARTSCRIPT_NAME = 'start_flower' # the name on the worker (inside _.BIN_PATH)
_.CELERY.FLOWERPORT             = "5555"


# NOT TRUE ANYMORE.. I HOPE PORTNUMERSS ECT WORK AS STRINGS AS WELL
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
#print 'found role: %s taks:%s' % (env.roles, env.tasks)

if len(env.tasks)==1 and len(env.roles)==1:
    
    task = env.tasks[0]
    role = env.roles[0]
    
    # WORKER related tasks
#    print '>%s<' % task
    if task in ['deploy_worker','update_worker_django', 'update_worker_glass']:
        
        _.ROLEDEFS = {
            'dev'   : {'hosts': _.WORKER_DEV_HOSTS},
            'test'  : {'hosts': _.WORKER_TEST_HOSTS}  ,      
            'prod'  : {'hosts': _.WORKER_PROD_HOSTS}  ,      
        }
        
        if role == 'dev':
            _.ROOT_PATH = '/tmp/app/swl_worker'
            _.BIN_PATH  = '/tmp/app/swl_worker_bin'
            _.TMPDIR    = '/tmp/app/swl_worker_tmp'
            _.SERVERHOST = "127.0.0.1"


        if role == "test":
            _.SERVERHOST = "127.0.0.1"
            
        if role == "prod":
            _.SERVERHOST = "swlabs.physik.uzh.ch" 
            
         
        if role in ['test', 'prod']:
            _.ROOT_PATH = '/home/ara/rafik/swlabs_worker'
            _.BIN_PATH  = '/home/ara/rafik/local_bins'
            _.TMPDIR    = '/home/ara/rafik/worker_tmp'
            
            

    # SERVER related tasks            
    elif task in ['deploy_server', 'update_server_django', 'test_srv', 'dbg_run']:
        
        _.ROLEDEFS = {
            'test'  : {'hosts': _.SERVER_TEST_HOST},
            'prod'  : {'hosts': _.SERVER_PROD_HOST},        
        }

        if role == 'dev':
            _.ROOT_PATH = '/tmp/swlabs'
            _.TMPDIR    = 'srv_tmp'
            
        elif role in ['test', 'prod']:
            _.ROOT_PATH = '/data/swlabs'
            _.TMPDIR    = 'srv_tmp'
            _.BIN_PATH  = '/data/swlabs/_bin'
            
        else:
            abort("role not found")
            
    else:
        abort("task not found: ROLEDEF inclomplete")
        
        

else:
    _.ROLEDEFS = {'dev': ''}


#
# WRITE DOWN THE ACTUAL CONFIG
# evaluates all the lambda funcion of keys with trailing _

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

    
def add_timestamp(_):
#    for k, v in _.items():
    for v in _.values():
        if isinstance(v, AttrDict):
            v.TIMESTAMP = env.TIMESTAMP
    return _

def flatten(_):
    __ = AttrDict()
    for k1, v1 in _.items():
        if isinstance(v1, AttrDict):
            for k2, v2 in v1.items():
                __[k1+'_'+k2] = v2
        else:
            __[k1] = v1
    return __
        
    

settings = add_timestamp(config_r(_))
flat_settings = flatten(settings)

#for k, v in settings.items():
#    print k, v

#for k, v in sorted(flat_settings.items()):
#    print k, v
