# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


#from django.utils import date
#from datetime import datetime

from lmt import tasks

#import simplejson as json

from ModellerApp.models import BasicLensData, ModellingResult
from ModellerApp.utils import EvalAndSaveJSON
from django.contrib.auth.models import User

import json


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
      data = json.dumps({"status":"BAD_JSON_DATA","desc":"the saveModel view couldn't access expected attributes in POST information"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response
    
    try:
      m = BasicLensData.objects.get(id=mid)

    except BasicLensData.DoesNotExist:
      data = json.dumps({"status":"BAD_MODELID_DOES_NOT_EXIST","desc":"the saveModel view couldn't the basic_data_obj you wanted to save a result for"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response

    u = User.objects.all()[0]
    
    obj = EvalAndSaveJSON(user_obj = u, # request.user,
                          data_obj= m,
                          jsonStr = st,
                          is_final= False)
    
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
  
  if res.is_rendered:
    #deliver images
    pass
  elif hasattr(res.task, id):
    #check status of task
    #if still running, return status
    #if finished:
    #delete task
    #set res.is_rendered = True
    #return image links
    pass
  else:
    #start the new task, retrun status information
    pass
  
  

  data = json.dumps({"status":"OK", "result_id":""})
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
  
  
  data = json.dumps({"status":"OK", "result_id":""})
  response = HttpResponse(data, content_type="application/json")
  
  response['Access-Control-Allow-Origin'] = "*"
  print "sending response"
  return response




@csrf_exempt
def getData(request):
  pass