# -*- coding: utf-8 -*-
"""
This is the config fork:
if the file 'machine_settings.py' is not present, load the dev settings.
Make sure on prod system, this file is generated

Created on Fri Jan  9 16:18:57 2015

@author: rafik
"""


from common_settings import *

try:
    from machine_settings import *
except ImportError:
    from machine_settings_dev import *
