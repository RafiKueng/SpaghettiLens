#from djcelery import celery
from celery import task

import time
import os
import subprocess


@task()
def calculateModel(result_id):
  print "we're in a task now, calculating a result"
  print '../tmp_media/'+str(result_id)+'/cfg.gls'
  print os.path.exists('../tmp_media/%06i/cfg.gls' % result_id)

  #retval = subprocess.call(['../glass/run_glass_dummy.py', '../tmp_media/'+str(result_id)+'/cfg.gls'])
  retval = subprocess.call(['../glass/run_glass', '../tmp_media/%06i/cfg.gls' % result_id])
  
  #time.sleep(x);
  print "glass has finished with retval: " + str(retval)
  return
