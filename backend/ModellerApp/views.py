# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import simplejson as sjson
#import simplejson as sjson

from celery.result import AsyncResult

#from django.utils import date
#from datetime import datetime

from lmt import tasks
from datetime import datetime

#import simplejson as json

from ModellerApp.models import BasicLensData, ModellingResult, Catalog
from ModellerApp.utils import EvalAndSaveJSON
from django.contrib.auth.models import User

from lmt.tasks import calculateModel

import json
import os


# this provides the client with a list of the catalogues and lenses
# available for modelling
@csrf_exempt
def getInitData(request):
  
  
  if request.method in ["GET", "POST"]:
    
    try:
      cs = Catalog.objects.values("id", "name", "description")
      lenses = BasicLensData.objects.values("id", "name", "catalog")

      jdata = sjson.dumps({"catalogues": list(cs), "lenses": list(lenses)})
      response = HttpResponse(jdata, content_type="application/json")
      
    except BasicLensData.DoesNotExist:
      response = HttpResponseNotFound("internal server error.. can't access teh models and catalogues", content_type="text/plain")
    
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



@csrf_exempt
def getSingeModelData(request, model_id):
  '''returns a single model from a request url /get_modeldata/1
  only for legacy, not really used anymore
  '''
  #print "in getModelData"
  
  #if request.method == "POST" or request.method == "GET":
  if request.method in ["GET", "POST"]:
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

  
  else:
    print "strange access"
    return HttpResponse("no post/get/otions request")  



@csrf_exempt
def getModelData(request):
  '''returns a model from a request url /get_modeldata/
  expects post with model ids and / or catalogue ids to work on for this session
  '''
  print "in new getModelData"
  
  if request.method in ["POST"]:
    #print "in post"
    #print "i got: ", str(request.POST)
    
    request.session['model_ids'] = [1,2,3]
    ids = request.session['model_ids']
    
    POST = request.POST
    session = request.session
    
    if "action" in POST:
      action = POST['action']
      
      if action == "init":
        print "init"
        print POST.get('models', " [none models] ")
        print POST.get('catalog', " [none cats] ")
        
        
        if "models" in POST and "catalog" in POST:
          print "error: got both, please decide"
        

        elif "models" in POST:
          print "got models"

          session["todo"] = POST['models']
          session["isInit"] = True
          
          m = BasicLensData.objects.get(id=model_id)
          
          
        elif "catalog" in POST:
          print "got catalog"
          
          session["todo"] = POST['models']
          session["isInit"] = True
          
          m = BasicLensData.objects.filter(catalog_id__exact=POST['catalog'])
          
          
        else:
          print "error: got neither model ids nor catalogues"
          
        
        session["isInit"] = True
        
      
      elif action == "prev" and session.get("isInit", False):
        print "get prev"
      
      elif action == "next" and session.get("isInit", False):
        print "get next"
      
      elif not session.get("isInit", False):
        print "bad request, not yet init.. (action:", action
        
      else:
        print "bad request, unknown action:", action
      
      
    else:
      print "bad request"
    
    
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

  
  else:
    print "strange access"
    return HttpResponse("no post/get/otions request")  



@csrf_exempt
def saveModel(request):
  if request.method == "POST":
    
    #print repr(request.POST)
    print "username:", request.user.username
    
    r = request.POST
    #print "Got Data: ", int(r['modelid']), r['string'], r['isFinal'] in ["True", "true"]
    #print r.__dict__
    
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
    print "eval and save"
    obj = EvalAndSaveJSON(user_obj = u, # request.user,
                          data_obj= m,
                          jsonStr = st,
                          is_final= False)
    print "after eval and save"
    #r.save()
    data = json.dumps({"status":"OK", "result_id": "%06i" % obj.result_id})
    response = HttpResponse(data, content_type="application/json")
      
    response['Access-Control-Allow-Origin'] = "*"
    print "sending response"
    return response



def loadModel(request):
  pass


@csrf_exempt
def getSimulationJSON(request, result_id):
  result_id = int(result_id)
  print "in getSimulationJSON"
  
  def returnDataIfReady():
    return json.dumps({"status":"READY",
                         "cached": True,
                         "result_id": "%06i" % result_id,
                         "n_img": 3,
                         "img1url": "/result/%06i/img1.png" % result_id,
                         "img1desc": "Contour Plot",
                         "img2url": "/result/%06i/img2.png" % result_id,
                         "img2desc": "Mass Distribution",
                         "img3url": "/result/%06i/img3.png" % result_id,
                         "img3desc": "Arrival Time Plot",
                         })
  
  try:
    res = ModellingResult.objects.get(id=result_id)
  except:
    raise
  #print res.__dict__
  
  imgExists = os.path.exists("../tmp_media/%06i/img1.png" % result_id)
  
  if res.is_rendered: #and imgExists: #nginx will catch this case for images, but not for the json objects..
    #deliver images
    # check imgExists: because a clean up prog could have deleted the files in the mean time and forgot to set the right flags in the db.. evil prog...

    data = returnDataIfReady()

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
      
      data = returnDataIfReady()

    elif task.state == "FAILURE":
      data = json.dumps({"status":"FAILURE", "result_id": "%06i" % result_id})
      
    else:
      data = json.dumps({"status":"PENDING", "result_id": "%06i" % result_id})
    
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
    data = json.dumps({"status":"STARTED", "result_id": "%06i" % result_id})
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
