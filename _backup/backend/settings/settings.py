#default setting
ROLE = "developpment_local"

# a helper class
class TODO(Exception):
    pass


# import basic settings
from base_settings import *

# import secrets
from secrets import *

# import machine configuration
from machine import *

#import version numbers
from version import *


if ROLE == "developpment_local":
  MODULE_DATABASE = "sqlite"
  MODULE_DJANGO = "dev"
  MODULE_STATIC = "xamp"
  MODULE_WORKER = "dummy"
  
elif ROLE == "developpment_server":
  MODULE_DATABASE = "sqlite"
  MODULE_DJANGO = "dev"
  MODULE_STATIC = "nginx"
  MODULE_WORKER = "celery"
  
elif ROLE == "production_server":
  MODULE_DATABASE = "mysql"
  MODULE_DJANGO = "gunicorn"
  MODULE_STATIC = "nginx"
  MODULE_WORKER = "celery"

elif ROLE == "production_worker":
  MODULE_DATABASE = "mysql"
  MODULE_DJANGO = "gunicorn"
  MODULE_STATIC = "nginx"
  MODULE_WORKER = "celery"
  
elif ROLE == "standalone_app":
  MODULE_DATABASE = "sqlite"
  MODULE_DJANGO = "cherrypi"
  MODULE_STATIC = "python"
  MODULE_WORKER = "multiprocessing"



# DATABASE MODULE SETTINGS
################################################################

if MODULE_DATABASE=="sqlite":
  DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.sqlite3',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
      'NAME': DATABASE_NAME,                      # Or path to database file if using sqlite3.
      'USER': '',                      # Not used with sqlite3.
      'PASSWORD': '',              # Not used with sqlite3.
      'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
      'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
  }

elif MODULE_DATABASE=="mysql":
  DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.mysql',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
      'NAME': DATABASE_NAME,                      # Or path to database file if using sqlite3.
      'USER': DATABASE_USER,                      # Not used with sqlite3.
      'PASSWORD': DATABASE_PASSWORD,              # Not used with sqlite3.
      'HOST': DATABASE_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
      'PORT': DATABASE_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
  }



# WORKER MODULE SETTINGS
################################################################


if MODULE_WORKER == "celery":
  import djcelery
  djcelery.setup_loader()
  
  INSTALLED_APPS += ('djcelery',)
  BROKER_URL = ('amqp://'+
                BROKER_USER+':'+BROKER_PASSWORD+
                '@'+BROKER_HOST+':'+str(BROKER_PORT)+'/'+BROKER_VHOST)
  CELERY_IMPORTS = ("lmt.tasks", )
  
  CELERYD_PREFETCH_MULTIPLIER = 1  #one worker get one task at a time, no reserving
  
elif MODULE_WORKER == "mp":
  pass

elif MODULE_WORKER == "dummy":
  pass

