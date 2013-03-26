SUPPORTED_OSES = ("deb", "win")

from fabric.api import env

def osSupported():
  return env.TARGET_OS in SUPPORTED_OSES

if env.TARGET_OS in SUPPORTED_OSES:

  # import the corresponding modules
  
  from ..modules.basic import basic as basic
  from ..modules.database import sqlite as database 
  from ..modules.django import dev as djangoserver
  from ..modules.static import xamp as staticserver
  from ..modules.worker import dummy as worker


def about():
  return "Setup a local developpment environment (no glass installed)"



        
        