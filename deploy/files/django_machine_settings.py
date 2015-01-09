# -*- coding: utf-8 -*-
"""
This file gets modified and automatically uploaded by the deploy script.
Make any changes there and re deploy!!! Don't do any manual changes here..


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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')ir@&^cmbu$e+btd&dske8h&u+u8dy9=mmho*tc171*0f!q@xn'
