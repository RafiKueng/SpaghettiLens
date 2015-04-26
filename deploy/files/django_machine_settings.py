# -*- coding: utf-8 -*-
"""
This file gets modified and automatically uploaded by the deploy script.
Make any changes there and re deploy!!! Don't do any manual changes here..
(esp. the settings.py file)

Created on %(timestamp)s
AUTOMATICALLY

@author: rafik
"""


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = %(DEBUG)s #True
TEMPLATE_DEBUG = %(TEMPLATE_DEBUG)s #True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : 'db.sqlite3',
        
    }
}

COUCHDB_DATABASES = (
#    ('djangoapp.spaghetti', 'http://192.168.100.3:5984/spaghetti'),
#    ('djangoapp.lenses',    'http://192.168.100.3:5984/lenses'),
    ('djangoapp.spaghetti', '%(COUCHSRV)s/spaghetti'),
    ('djangoapp.lenses',    '%(COUCHSRV)s/lenses'),
)

#STATIC_ROOT = '/data/swlabs/static'
#MEDIA_ROOT = '/data/swlabs/media'

#UPLOAD_USER = 'rafik'
#UPLOAD_HOST = '192.168.100.10'

STATIC_ROOT = '%(STATIC_ROOT)s'
MEDIA_ROOT = '%(MEDIA_ROOT)s'

UPLOAD_USER = '%(UPLOAD_USER)s'
UPLOAD_HOST = '%(UPLOAD_HOST)s'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%(SECRET_KEY)s'

# Celery / Broker Configuration
#BROKER_URL = 'amqp://guest:guest@192.168.100.3:5672/swlabs'
#CELERY_RESULT_BACKEND = 'amqp://guest:guest@192.168.100.3:5672/swlabs/'

BROKER_URL = '%(CELERY_URL)s'
CELERY_RESULT_BACKEND = '%(CELERY_URL)s'
