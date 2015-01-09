# -*- coding: utf-8 -*-
"""
Default values for config. Used on dev site.
this file will not beloaded, if a 'machine_settings.py' is present

Created on Fri Jan  9 16:25:31 2015
@author: rafik
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')ir@&^cmbu$e+btd&dske8h&u+u8dy9=mmho*tc171*0f!q@xn'
DATABASES['default']['password'] = ''
