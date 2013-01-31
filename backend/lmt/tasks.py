#from djcelery import celery
from celery import task

import time


#@celery.task
@task()
def calculateModel(x):
  time.sleep(x);
  return "slept for %f secs" % x