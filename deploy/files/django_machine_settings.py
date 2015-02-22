# -*- coding: utf-8 -*-
"""
This file gets modified and automatically uploaded by the deploy script.
Make any changes there and re deploy!!! Don't do any manual changes here..
(esp. the settings.py file)

Created on Fri Jan  9 16:25:31 2015
@author: rafik
"""


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : 'db.sqlite3',
        
    }
}

COUCHDB_DATABASES = (
    ('djangoapp.spaghetti', 'http://192.168.100.3:5984/spaghetti'),
    ('djangoapp.lenses',    'http://192.168.100.3:5984/lenses'),
)

STATIC_ROOT = '/data/swlabs/static'
MEDIA_ROOT = '/data/swlabs/media'

UPLOAD_USER = 'rafik'
UPLOAD_HOST = '192.168.100.10'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')ir@&^cmbu$e+btd&dske8h&u+u8dy9=mmho*tc171*0f!q@xn'

# Celery / Broker Configuration
BROKER_URL = 'amqp://guest:guest@192.168.100.3:5672/swlabs'
CELERY_RESULT_BACKEND = 'amqp://guest:guest@192.168.100.3:5672/swlabs/'
