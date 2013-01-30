#from djcelery import celery
from celery import task

import time


#@celery.task
@task()
def calculateModel(x, y):
  time.sleep(y);
  return x + y