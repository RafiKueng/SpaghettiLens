SUPPORTED_OSES = ("deb")

from fabric.api import env

def osSupported():
  return env.TARGET_OS in SUPPORTED_OSES

if env.TARGET_OS in SUPPORTED_OSES:
  # import the corresponding modules
  from ..modules.basic import basic as basic
  from ..modules.database import sqlite as database
  from ..modules.django import dev as djangoserver
  from ..modules.static import python as staticserver
  from ..modules.worker import celery as worker


def about():
  return "Setup a remote developpment environment (everything is set up, but dev versions of the servers are used)"
