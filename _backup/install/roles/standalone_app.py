SUPPORTED_OSES = ("deb")

from fabric.api import env

def osSupported():
  return env.TARGET_OS in SUPPORTED_OSES

if env.TARGET_OS in SUPPORTED_OSES:
  # import the corresponding modules
  from ..modules import basic as basic 
  from ..modules.database import sqlite as database 
  from ..modules.django import cherrypi as djangoserver
  from ..modules.static import python as staticserver
  from ..modules.worker import multiprocessing as worker


def about():
  return "Setup a local standalone app"