import time
import os
import subprocess
import socket

from django.conf import settings as s



if s.MODULE_WORKER == "celery":
  #from djcelery import celery
  from celery import task, current_task

  if s.ROLE == "production_worker":
    @task()
    def calculateModel(result_id):
      rq = current_task.request
      print "TASK (expires:",rq.expires,', kwargs:', rq.kwargs #, ', options', rq.options
      #myname = socket.gethostname()

      retval = subprocess.call(['../run_worker_glass', '%06i' % result_id])
      
      #time.sleep(x);
      print "glass has finished with retval: " + str(retval)
      return
    
  else: 
    @task()
    def calculateModel(result_id):
      rq = current_task.request
      print "TASK (expires:",rq.expires,', kwargs:', rq.kwargs #, ', options', rq.options
      #print "we're in a task now, calculating a result"
      #print '../tmp_media/'+str(result_id)+'/cfg.gls'
      #print os.path.exists('../tmp_media/%06i/cfg.gls' % result_id)
      os.chdir(s.WORKER_DIR_FULL)
      #retval = subprocess.call(['../glass/run_glass_dummy.py', '../tmp_media/'+str(result_id)+'/cfg.gls'])
      retval = subprocess.call(['%s/run_glass' % s.WORKER_DIR_FULL, '../tmp_media/%06i/cfg.gls' % result_id])
      
      #time.sleep(x);
      print "glass has finished with retval: " + str(retval)
      return



elif s.MODULE_WORKER == "multiprocessing":
  class calculateModel_MP:
    task_id = 99999
    state = "SUCCESS"
    def __init__(self):
      print "creating a new dummy task"
    def delay(self, resnr):
      return True
    
  calculateModel = calculateModel_MP()
  

elif s.MODULE_WORKER == "dummy":
  class calculateModel_D:
    task_id = "#001"
    state = "SUCCESS"
    def __init__(self):
      print "creating a new dummy task"
    def __call__(self, resid):
      return self
    def delay(self, resnr):
      print "starting the dummy task1"
      self.result_id = resnr
      
      # create dummy files
      for i in range(1,4):
        with open('../tmp_media/%06i/img%i.png'%(resnr,i), 'w') as f:
          f.write(str(i))
      return self
    
    
    def apply_async(self, *args, **kwargs):
      
      print "starting the dummy task2", args, kwargs
      rid = kwargs['args'][0]
      # create dummy files
      #os.mkdir('..\\tmp_media\\%06i\\'%rid)
#      for i in range(1,4):
#        with open('../tmp_media/%06i/img%i.png'%(rid,i), 'w') as f:
#          f.write(str(i))
      import shutil
      shutil.copyfile('../tmp_media/1.png','../tmp_media/%06i/img1.png'%(rid) )
      shutil.copyfile('../tmp_media/2.png','../tmp_media/%06i/img2.png'%(rid) )
      shutil.copyfile('../tmp_media/3.png','../tmp_media/%06i/img3.png'%(rid) )
      shutil.copyfile('../tmp_media/4.png','../tmp_media/%06i/img3_ipol.png'%(rid) )
      self.result_id = rid
      return self
    
  

  calculateModel = calculateModel_D()
  DummyAsyncResult = calculateModel
  

