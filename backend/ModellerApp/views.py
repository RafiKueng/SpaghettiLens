# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from celery.result import AsyncResult

#from django.utils import date
#from datetime import datetime

from lmt import tasks
from datetime import datetime

#import simplejson as json

from ModellerApp.models import BasicLensData, ModellingResult
from ModellerApp.utils import EvalAndSaveJSON
from django.contrib.auth.models import User

from lmt.tasks import calculateModel

import json
import os


@csrf_exempt
def getModelData(request, model_id):
  
  #print "in getModelData"
  
  if request.method == "POST":
    #print "in post"
    #print "i got: ", str(request.POST)
    
    try:
      m = BasicLensData.objects.get(id=model_id)
      data = serializers.serialize("json", [m])
      response = HttpResponse(data, content_type="application/json")
    except BasicLensData.DoesNotExist:
      response = HttpResponseNotFound("this model is not available", content_type="text/plain")
      
    response['Access-Control-Allow-Origin'] = "*"
    return response
  
  
  elif request.method == "OPTIONS":
    #print "in options"  
    response = HttpResponse("")
    response['Access-Control-Allow-Origin'] = "*"
    response['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
    response['Access-Control-Allow-Headers'] = "x-requested-with, x-requested-by"
    response['Access-Control-Max-Age'] = "180"
    return response
  
  
  elif request.method == "GET":
    print "in get"
    return HttpResponse("in GET")  
  
  else:
    print "in neither"
    return HttpResponse("no post request")  




@csrf_exempt
def saveModel(request):
  if request.method == "POST":
    
    print repr(request.POST)
    print request.user.username
    
    r = request.POST
    #print "Got Data: ", int(r['modelid']), r['string'], r['isFinal'] in ["True", "true"]
    try:
      mid = int(r['modelid'])
      st = r['string']
      isf = r['isFinal'] in ["True", "true"]
    except KeyError:
      print "KeyError in save model"
      data = json.dumps({"status":"BAD_JSON_DATA","desc":"the saveModel view couldn't access expected attributes in POST information"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response
    
    try:
      m = BasicLensData.objects.get(id=mid)

    except BasicLensData.DoesNotExist:
      print "BLD not found in save model"
      data = json.dumps({"status":"BAD_MODELID_DOES_NOT_EXIST","desc":"the saveModel view couldn't the basic_data_obj you wanted to save a result for"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response

    u = User.objects.all()[0]
    print "evaland save"
    obj = EvalAndSaveJSON(user_obj = u, # request.user,
                          data_obj= m,
                          jsonStr = st,
                          is_final= False)
    print "after eval and save"
    #r.save()
    data = json.dumps({"status":"OK", "result_id":obj.result_id})
    response = HttpResponse(data, content_type="application/json")
      
    response['Access-Control-Allow-Origin'] = "*"
    print "sending response"
    return response



def loadModel(request):
  pass


@csrf_exempt
def getSimulationJSON(request, result_id):
  print "in getSimulationJSON"
  
  try:
    res = ModellingResult.objects.get(id=result_id)
  except:
    raise
  print res.__dict__
  
  imgExists = os.path.exists("../tmp_media/"+str(result_id)+"/img1.png")
  
  if res.is_rendered: #and imgExists: #nginx will catch this case for images, but not for the json objects..
    #deliver images
    # check imgExists: because a clean up prog could have deleted the files in the mean time and forgot to set the right flags in the db.. evil prog...
    data = json.dumps({"status":"READY",
                         "cached": True,
                         "result_id":result_id,
                         "n_img": 3,
                         "img1url": "/result/"+str(result_id)+"/img1.png",
                         "img1desc": "Contour Lines",
                         "img1url": "/result/"+str(result_id)+"/img1.png",
                         "img1desc": "Contour Lines",
                         "img1url": "/result/"+str(result_id)+"/img1.png",
                         "img1desc": "Contour Lines",
                         "img1url": "/result/"+str(result_id)+"/img1.png",
                         "img1desc": "Contour Lines"
                         })
    res.last_accessed = datetime.now()
    res.save()

  elif not isinstance(res.task_id, type(None)) and len(res.task_id) > 2:
    print "task is started already"

    task = AsyncResult(res.task_id)
    print "status: ", task.state
    
    if task.state == "SUCCESS":
      res.task_id = "";
      res.is_rendered = True;
      res.last_accessed = datetime.now()
      res.save()
      
      data = json.dumps({"status":"READY",
                         "result_id":result_id,
                         "n_img": 1,
                         "img1url": "/result/"+str(result_id)+"/img1.png",
                         "img1desc": "Contour Lines"
                         })
    else:
      data = json.dumps({"status":"PENDING", "result_id":result_id})
    
  else:
    print "starting new task"
    print result_id
    print type(result_id)
    task = calculateModel.delay(result_id)
    res.is_rendered = False
    res.task_id = task.task_id
    res.rendered_last = datetime.now();
    res.save()
    #start the new task, retrun status information
    data = json.dumps({"status":"STARTED", "result_id":result_id})
    pass
  
  


  response = HttpResponse(data, content_type="application/json")
  
  response['Access-Control-Allow-Origin'] = "*"
  print "sending response"
  return response



@csrf_exempt
def getSimulationFiles(request, result_id, filename):
  
  print 'result_id: %s; filename: %s'%(result_id, filename)
  
  # if filename on harddisk tmp dir > deliver
  # if not:
  #   kick of task to create the files
  #  check task every 10sec for one minute
  #  if no answer till then, redirect so same url and start again
  
  
  data = json.dumps({"status":result_id, "result_id":filename})
  response = HttpResponse(data, content_type="application/json")
  
  response['Access-Control-Allow-Origin'] = "*"
  print "sending response"
  return response




@csrf_exempt
def getData(request):
  pass