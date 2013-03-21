SUPPORTED_OSES = ("deb")

from fabric.api import env
def osSupported():
  return env.TARGET_OS in SUPPORTED_OSES

if env.TARGET_OS in SUPPORTED_OSES:
  # import the corresponding modules
  from ..modules.basic import basic as basic 
  from ..modules.database import mysql as database 
  from ..modules.django import gunicorn as djangoserver
  from ..modules.static import nginx as staticserver
  from ..modules.worker import celery as worker


def about():
  return "production setup, uses production level servers, minifies code ect..."


def neededVars():
  return (
    ("INSTALL_DIR", "where to install the server (absolute path)", "/srv/lmt"),
  )