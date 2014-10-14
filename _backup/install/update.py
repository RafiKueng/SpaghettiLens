import os

from fabric.api import local, settings, abort, run, cd, env, sudo
from fabric.utils import puts
from fabric.operations import prompt
from fabric.contrib.console import confirm
from package import *
from virtualenv import *
from utils import _r, _s, _cd


from importlib import import_module
import pkgutil

import roles as roles_mod



conf = {}

env.conf = conf


def update():
  import roles.production_server as ps
  
  import modules.basic.basic as basic
  import modules.databse.mysql as database
  import modules.django.gunicorn as django
  import modules.static.nginx as static
  import modules.worker.celery as worker

  mods = [ps, django, static, worker]
  
  for mod in mods:
    try:
      mod.update()
    except AttributeError as e:
      if e.message != "'module' object has no attribute 'update'":
        raise
        
    
  for mod in mods:
    try:
      mod.reload()
    except AttributeError as e:
      if e.message != "'module' object has no attribute 'reload'":
        raise
