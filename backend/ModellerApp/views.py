# Create your views here.
from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import simplejson as sjson
from django.utils.timezone import now
from django.conf import settings as s



from lmt import tasks
import random

from ModellerApp.models import LensData, BasicLensData, ModellingResult, Catalog
from ModellerApp.utils import EvalAndSaveJSON
from django.contrib.auth.models import User

from lmt.tasks import calculateModel
if s.MODULE_WORKER == "celery":
  from celery.result import AsyncResult
elif s.MODULE_WORKER == "multiprocessing":
  raise s.TODO("mp modules missing")
  from lmt.tasks import bla as AsyncResult
elif s.MODULE_WORKER == "dummy":
  from lmt.tasks import DummyAsyncResult as AsyncResult


import datasources

import os


# this provides the client with a list of the catalogues and lenses
# available for modelling
@csrf_exempt
def getInitData(request):
  
  request.session.set_test_cookie()
  
  
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
  #print "in getSingleModelData"
  #print 'testcookie:', request.session.test_cookie_worked()

  # check if cookies enabled: disabled in debug
  print 'debug:',  DEBUG
  if not lmt.settings.DEBUG:
    if not request.session.test_cookie_worked():
      response = HttpResponseNotFound("Cookies not enabled, please enable", content_type="text/plain")
      response['Access-Control-Allow-Origin'] = "*"
      return response
  
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
#  print 'testcookie:', request.session.test_cookie_worked()
  
  if request.method in ["POST"]:
    print "in post"
    print "i got: ", str(request.POST)
    print "session has: ", str(request.session.__dict__)


    if not s.DEBUG:
      if not request.session.test_cookie_worked():
        response = HttpResponseNotFound("Cookies not enabled, please enable", content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response

    
    #request.session['model_ids'] = [1,2,3]
    #ids = request.session['model_ids']
    
    POST = request.POST
    session = request.session
    
    if "action" in POST:
      action = POST['action']
      
      if action == "init":
        print "init"
        print POST.getlist('models[]', " [none models] ")
        print POST.get('catalog', " [none cats] ")
        
        
        if "models[]" in POST:
          print "got models"

          list = [int(x) for x in POST.getlist('models[]', [])]
          

        elif "catalog" in POST:
          print "got catalog"
          cid = int(POST.get('catalog', "0"))
          m = BasicLensData.objects.filter(catalog__pk__exact=cid)
          vals = m.values('id')
          list = [x['id'] for x in vals]
                 
        else:
          print "error, no models supplied"
          response = HttpResponseNotFound("wrong post format, model[] expected", content_type="text/plain")
          response['Access-Control-Allow-Origin'] = "*"
          return response

        print "list", list

        todolist = [{'id':x, 'isDone':False, 'stateId':None} for x in list]
        nextElem, listElem, todolist = _getNextFromList(todolist)
        
        session["lensesTodo"] = todolist
        session["workingOn"] = listElem
        session["lensesDone"] = []
        

        session["isInit"] = True
        
        nextId = listElem['id']
        

 

      elif action == "cont" and session.get("isInit", False):
        print "continue previous session"
        #TODO: implement user sessions
      

      
      
      elif action == "prev" and session.get("isInit", False):
        print "get prev"
        
        todo = session["lensesTodo"]
        done = session["lensesDone"]
        work = session["workingOn"]
        
        todo.append(work)
        work = done.pop()
        
        session["lensesTodo"] = todo
        session["lensesDone"] = done
        session["workingOn"] = work
        
        nextId = work['id']
        try:
          nextElem = LensData.objects.get(id=nextId)
        except LensData.DoesNotExist:
          response =  HttpResponseNotFound("for some reason you have an ivalid model in your list", content_type="text/plain")
          response['Access-Control-Allow-Origin'] = "*"
          return response        


      
      elif action == "next" and session.get("isInit", False):
        print "get next"

        todo = session["lensesTodo"]
        done = session["lensesDone"]
        work = session["workingOn"]

        done.append(work)
        nextElem, work, todo = _getNextFromList(todo)

        session["lensesTodo"] = todo
        session["lensesDone"] = done
        session["workingOn"] = work

        nextId = work['id']
  
        
      
      elif not session.get("isInit", False):
        print "bad request, not yet init.. (action:", action
        
        response = HttpResponseNotFound("this model is not available", content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response        

      else:
        print "bad request, unknown action:", action
        response = HttpResponseNotFound("bad request, unknown action", content_type="text/plain")
        response['Access-Control-Allow-Origin'] = "*"
        return response        

      
      print "nextId", nextId
      
      try:
        #m = BasicLensData.objects.get(id=nextId)
        #nDone = sum(session["isLensDone"])
        #nLenses = len(list)
        #nTodo = nLenses - nDone
        #n = {'todo': nTodo,
        #     'done': nDone,
        #     'nr': nLenses,
        #     'next_avail': workingOn < len(list)-1,
        #     'prev_avail': workingOn > 0}
        
        nextElem.requested_last = now()
        nextElem.save()
        
        nDone = len(session["lensesDone"])
        nTodo = len(session["lensesTodo"])
        nLenses = nDone + nTodo
        n = {'todo': nTodo+1, # and the current
             'done': nDone,
             'nr': nLenses,
             'next_avail': nTodo>0,
             'prev_avail': nDone >0}
        data1 = serializers.serialize("json", [nextElem])
        data2 = sjson.dumps(n)
        #print "data1", data1
        print "data2", data2
        
        data = data1[0:-1] + ',' + data2 + ']'
        
        response = HttpResponse(data, content_type="application/json")
      except BasicLensData.DoesNotExist:
        response = HttpResponseNotFound("this model is not available", content_type="text/plain")

      response['Access-Control-Allow-Origin'] = "*"
      print "session has", str(request.session.__dict__)
      return response        
      
      
    else:
      print "bad request"
      response = HttpResponseNotFound("this was a bad request", content_type="text/plain")
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
    response = HttpResponseNotFound("no post/get/otions request", content_type="text/plain")
    response['Access-Control-Allow-Origin'] = "*"
    return response   


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
      user = r['username']

      
    except KeyError:
      print "KeyError in save model"
      data = sjson.dumps({"status":"BAD_JSON_DATA","desc":"the saveModel view couldn't access expected attributes in POST information"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response
    
    try:
      m = LensData.objects.get(id=mid)

    except LensData.DoesNotExist:
      print "LensData obj not found (in save model)"
      data = sjson.dumps({"status":"BAD_MODELID_DOES_NOT_EXIST","desc":"the saveModel view couldn't the basic_data_obj you wanted to save a result for"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response

    u = User.objects.all()[0]
    print "eval and save"
    obj = EvalAndSaveJSON(user_obj = u, # request.user,
                          user_str = user,
                          data_obj= m,
                          jsonStr = st,
                          is_final= isf)
    print "after eval and save"
    #r.save()
    
    data = sjson.dumps({"status":"OK", "result_id": "%06i" % obj.result_id})
    response = HttpResponse(data, content_type="application/json")
      
    response['Access-Control-Allow-Origin'] = "*"
    print "sending response"
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
def saveModelFinal(request):
  print "in savemodelfinal"
  if request.method == "POST":
    r = request.POST
    #print "Got Data: ", int(r['modelid']), r['string'], r['isFinal'] in ["True", "true"]
    #print r.__dict__
    
    try:
      mid = int(r['modelid'])
      rid = int(r['resultid'])
      isf = r['isFinal'] in ["True", "true"]

    except KeyError:
      print "KeyError in save model final"
      data = sjson.dumps({"status":"BAD_JSON_DATA","desc":"the saveModel view couldn't access expected attributes in POST information"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response

    if not isf:
      print "is not final in save model final"
      data = sjson.dumps({"status":"BAD_PARMS","desc":"the saveModelFinal view called with no final result"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response

    try:
      m = BasicLensData.objects.get(id=mid)
      r = ModellingResult.objects.get(id=rid)
    except:
      print "keyerror in save model final"
      data = sjson.dumps({"status":"BAD_KEYS","desc":"blabla"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response      
    
    if m.n_res: m.n_res = m.n_res + 1
    else: m.n_res = 1
    
    r.is_final_result = True
    m.save()
    r.save()

    data = sjson.dumps({"status":"OK", "result_id": "%06i" % rid})
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
  
  def returnDataIfReady(result_id):
    return sjson.dumps({"status":"READY",
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

    data = returnDataIfReady(result_id)

    res.last_accessed = now()
    res.save()

  elif not isinstance(res.task_id, type(None)) and len(res.task_id) > 2:
    print "task is started already"

    task = AsyncResult(res.task_id)
    print "status: ", task.state
    
    if task.state == "SUCCESS":
      res.task_id = "";
      res.is_rendered = True;
      res.last_accessed = now()
      res.save()
      
      data = returnDataIfReady(result_id)

    elif task.state == "FAILURE":
      data = sjson.dumps({"status":"FAILURE", "result_id": "%06i" % result_id})
      
    else:
      data = sjson.dumps({"status":"PENDING", "result_id": "%06i" % result_id})
    
  else:
    print "starting new task"
    # print result_id
    # print type(result_id)
    task = calculateModel.delay(result_id)
    res.is_rendered = False
    # print task.task_id, type(task.task_id)
    res.task_id = task.task_id
    res.rendered_last = now();
    res.save()
    #start the new task, retrun status information
    data = sjson.dumps({"status":"STARTED", "result_id": "%06i" % result_id})
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
  
  
  data = sjson.dumps({"status":result_id, "result_id":filename})
  response = HttpResponse(data, content_type="application/json")
  
  response['Access-Control-Allow-Origin'] = "*"
  print "sending response"
  return response




@csrf_exempt
def getData(request, result_id):
  result_id = int(result_id)
  print "in getData"
  
  try:
    res = ModellingResult.objects.get(id=result_id)
    if res.is_rendered: #and imgExists: #nginx will catch this case for images, but not for the json objects..
      #deliver images
      # check imgExists: because a clean up prog could have deleted the files in the mean time and forgot to set the right flags in the db.. evil prog...
  
      res.last_accessed = now()
      res.save()
      
      html = '''
<html>
<head></head>
<body>
  <h1>Result Nr %(rid)i for %(obj_name)s</h1>
  <p>%(rid_str)s<br />
  %(obj_str)s</p>
  <img src="/result/%(rid)06i/img3.png" alt="ArrTPlot">
  <h2>Lens Image:</h2>
  <img src="%(obj_url)s" alt="LensURL">
  <h2>Contour Plot:</h2>
  <img src="/result/%(rid)06i/img1.png" alt="ContPlot">
  <h2>Mass Distribution Plot:</h2>
  <img src="/result/%(rid)06i/img2.png" alt="MDistrPlot">
  <h2>Arrival Time Plot:</h2>
  <img src="/result/%(rid)06i/img3.png" alt="ArrTPlot">
  <h2>Model JSON:</h2>
  <p>%(mstr)s</p>
</body>
</html>''' % {'rid': result_id,
                'mstr': res.json_str,
                'rid_str': res.__unicode__(),
                'obj_name': res.lens_data_obj.name,
                'obj_str': res.lens_data_obj.__unicode__(),
                'obj_url': sjson.loads(res.lens_data_obj.img_data)['url']
                } 
  
    else:
      raise
  except:
    print "some error in getting result data overview"
    html = "<html><head></head><body>no data available</body></html>"
  
  
  response = HttpResponse(html)
  
  response['Access-Control-Allow-Origin'] = "*"
  print "sending response"
  return response





############### helper ##########################


def _getNextFromList(list):
  ''' returns the next element to work on '''
  purelist = [x['id'] for x in list]
  
  #print "in getnext"
  #print list
  #print purelist
  
  n = LensData.objects.filter(id__in=purelist) # select all in list
  #m = n.annotate(n_res=Count('modellingresult')) # sum up the results, save in n_res
  #m = n.order_by('n_res')
  min = n.aggregate(Min('n_res')) # get the min of n_res
  a = n.filter(n_res=min['n_res__min']) # get those with minimal results
  b = a.order_by('last_accessed')[0] # order those by the date of last access, get the last
  #c = random.choice(b)
  
  id = b.id
  listpos = purelist.index(id)
  listElem = list.pop(listpos)
  
  #print min
  #print 'a'
  #for x in a: print a
  #print "b", b.id, b
  
  
  return b, listElem , list




@csrf_exempt
def api(request):
  if request.method in ["POST"]:
    
    request.session.set_test_cookie()

    if request.session.test_cookie_worked():
      #request.session.delete_test_cookie()
      print "session works"
    else:
      print "session doesn't work"

    try:
      post = request.POST
      print post
      
      if post['action'] == 'getSrcList':
        resp = _getSrcList()
      elif post['action'] == 'selectSource':
        resp = _selectSource(request, int(post['id']), post['uname'])
      elif post['action'] == 'datasourceApi':
        resp = _datasourceApi(request, int(post['src_id']))
      elif post['action'] == 'saveModel':
        resp = _saveModel(request)
      elif post['action'] == 'getBla':
        resp = _getBla()
      elif post['action'] == 'getBla':
        resp = _getBla()
      elif post['action'] == 'getBla':
        resp = _getBla()
      else:
        resp = HttpResponseNotFound("no valid post request parameters")
      
      resp['Access-Control-Allow-Origin'] = "*"      
      return resp
        
      
      
    except:
      
      response = HttpResponseNotFound("no post request", content_type="text/plain")
      raise
    
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
    return HttpResponseNotFound("internal server error.. can't access teh models and catalogues", content_type="text/plain")
    



def _getSrcList():
  m = [{'id': _[0], 'desc': _[1], 'mod': _[2]} for _ in datasources.members]
  data = sjson.dumps(m)
  return HttpResponse(data, content_type="application/json")


def _selectSource(request, id, username):
  sourceModule = datasources.members[id][3]
  request.session['datasource_id'] = id
  request.session['username'] = username
  return HttpResponse(sjson.dumps(sourceModule.getDialog()), content_type="application/json")

def _datasourceApi(request, src_id):
  print "this session:"
  print request.session.items()
  try:
    id = request.session['datasource_id']
  except: # TODO: remove except: this cause is only here for local dev.. (no sessions)
    print "no session found"
    id = src_id
  sourceModule = datasources.members[int(id)][3]
  return HttpResponse(sjson.dumps(sourceModule.api(request.POST)), content_type="application/json")











def _saveModel(request):
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
      user = r['username']

      
    except KeyError:
      print "KeyError in save model"
      data = sjson.dumps({"status":"BAD_JSON_DATA","desc":"the saveModel view couldn't access expected attributes in POST information"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response
    
    try:
      m = LensData.objects.get(id=mid)

    except LensData.DoesNotExist:
      print "LensData obj not found (in save model)"
      data = sjson.dumps({"status":"BAD_MODELID_DOES_NOT_EXIST","desc":"the saveModel view couldn't the basic_data_obj you wanted to save a result for"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response

    u = User.objects.all()[0]
    print "eval and save"
    obj = EvalAndSaveJSON(user_obj = u, # request.user,
                          user_str = user,
                          data_obj= m,
                          jsonStr = st,
                          is_final= isf)
    print "after eval and save"
    #r.save()
    
    data = sjson.dumps({"status":"OK", "result_id": "%06i" % obj.result_id})
    response = HttpResponse(data, content_type="application/json")
      
    response['Access-Control-Allow-Origin'] = "*"
    print "sending response"
    return response
