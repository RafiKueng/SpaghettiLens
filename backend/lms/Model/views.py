# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
#from django.utils import date
from datetime import datetime

from lms import tasks

#import simplejson as json

from Model.models import ModelData, Result

import json

@csrf_exempt
def getModelData(request, model_id):
  
  #print "in getModelData"
  
  if request.method == "POST":
    #print "in post"
    #print "i got: ", str(request.POST)
    
    try:
      m = ModelData.objects.get(id=model_id)
      data = serializers.serialize("json", [m])
      response = HttpResponse(data, content_type="application/json")
    except ModelData.DoesNotExist:
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
    
    #print repr(request.POST)
    
    r = request.POST
    #print "Got Data: ", int(r['modelid']), r['string'], r['isFinal'] in ["True", "true"]
    mid = int(r['modelid'])
    st = r['string']
    isf = r['isFinal'] in ["True", "true"]
    
    m = ModelData.objects.get(id=mid)
    r = Result(  model= m,
                 string = st,
                 isFinalResult = isf)
    try:
      r.save()
      data = json.dumps({"status":"OK"})

      response = HttpResponse(data, content_type="application/json")
    except:
      data = json.dumps({"status":"BAD__JSON_DATA_INVALID_OR_MODEL_NOT_FOUND"})
      response = HttpResponseNotFound("error", content_type="application/json")
      
    response['Access-Control-Allow-Origin'] = "*"
    return response



def loadModel(request):
  pass

def calcModel(request):
  tsk = tasks.calculateModel.delay(4, 5)
  
  pass