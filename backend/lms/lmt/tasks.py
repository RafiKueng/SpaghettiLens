from djcelery import celery

import time


@celery.task
def calculateModel(x, y):
  time.sleep(y);
  return x + y