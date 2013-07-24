# Create your views here.
from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import simplejson as sjson
from django.utils.timezone import now
from django.conf import settings as s
from django.shortcuts import render
from django.http import Http404

from lmt import tasks

import random
from math import exp

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
      pid = int(r['parentid'])

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
      m = LensData.objects.get(id=mid)
      res = ModellingResult.objects.get(id=rid)
    except:
      print "keyerror in save model final"
      data = sjson.dumps({"status":"BAD_KEYS","desc":"blabla"})
      response = HttpResponseNotFound(data, content_type="application/json")
      response['Access-Control-Allow-Origin'] = "*"
      return response
    
    try:
      #print "imgdata", r['imgData'][0:200]
      imgstr = r['imgData']
      ident, img = imgstr.split(',')
      #print ident
      if ident == "data:image/png;base64" and img.startswith('iVBORw0KGgo'):
        fh = open("../tmp_media/%06i/input.png" % rid, "wb")
        fh.write(img.decode('base64'))
        fh.close()
      else:
        print 'Error: no image upload'
    except:
      print 'Could not open/write file'
    
    if m.n_res: m.n_res = m.n_res + 1
    else: m.n_res = 1
    
    if pid>-1:
      try:
        pres = ModellingResult.objects.get(id=pid)
        res.parent_result = pres
      except:
        pass
    
    res.is_final_result = True
    m.save()
    res.save()

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

    elif task.state == "REVOKED":
      data = sjson.dumps({"status":"REVOKED", "result_id": "%06i" % result_id})
      
    else:
      data = sjson.dumps({"status":"PENDING", "result_id": "%06i" % result_id})
    
  else:
    #calculating the time limits
    pr = res.pixrad
    nm = res.n_models
    dt = (0.108 * exp(0.506*pr) + 0.01 * nm + 0.5) * 2 + 30
    dt = 60*15
    expire = 30 # a task won't run if it's been more than 30s in the queue

    #print "starting new task with timeout:", dt 
    # print result_id
    # print type(result_id)
    #task = calculateModel.delay(result_id)
    
    task = calculateModel.apply_async(args=(result_id,), timeout=dt, expires=expire)
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



import os.path

@csrf_exempt
def getData(request, result_id):
  print "in getData"
  
  result_id = int(result_id)
  try:
    res = ModellingResult.objects.get(id=result_id)
  except ModellingResult.DoesNotExist:
    raise Http404


  try:
    ldata = res.lens_data_obj
    lensdataitems = [
      ('Id', ldata.pk),
      ('Name', ldata.name),
      ('From', ldata.datasource),
      #('Saved by', ldata.created_by_str)
    ]
    lensimg = sjson.loads(ldata.img_data)['url']
  except:
    print 'error'
    lensdataitems = None
    lensimg = None

  
  res.last_accessed = now()
  res.save()
  
  def checkFile(resnr, name):
    path = "../tmp_media/%06i/%s" % (resnr, name)
    #print "checking path", path,
    if os.path.isfile(path):
      #print "exists"
      return "/result/%06i/%s" % (resnr, name)
    else:
      #print "nope"
      return None
  
  file_inp = checkFile(result_id, 'input.png')
  file_1 = checkFile(result_id, 'img1.png')
  file_2 = checkFile(result_id, 'img2.png')
  file_3 = checkFile(result_id, 'img3.png')
  file_4 = checkFile(result_id, 'img4.png')
  file_gls = checkFile(result_id, 'cfg.gls')
  file_state = checkFile(result_id, 'state.txt')
  file_log = checkFile(result_id, 'log.txt')

  # if one doesn't exist, recalulate the model
  refresh = False  
  if not (file_1 and file_2 and file_3): #file_4
    #TODO: if state exists, only create images

    print "getData: sone images missing, should recalculate"

    if not isinstance(res.task_id, type(None)) and len(res.task_id) > 2:
      print "task is started already"
  
      task = AsyncResult(res.task_id)
      print "status: ", task.state
      
      if task.state == "SUCCESS":
        #TODO: it could be that this point is never reached, take care of it!!
        res.task_id = "";
        res.is_rendered = True;
        res.last_accessed = now()
        res.save()
        refresh = False
      # task failed
      elif task.state == "FAILURE":
        refresh = False
      
      # task is still running
      else:
        refresh = 30
      
    else:
      print "starting new task"
      task = calculateModel.delay(result_id)
      res.is_rendered = False
      res.task_id = task.task_id
      res.rendered_last = now();
      res.save()
      pass
      refresh = 60
  
  
  parent = res.parent_result
  if parent:
    parent_data = {
      'nr':   parent.pk,
      'user': parent.created_by_str,
      'date': parent.created
    }
  else:
    parent_data = None
    
  children = res.child_results.all()
  #print "found x children", children
  
  if children.count() > 0:
    children_data = []
    for child in children:
      children_data.append({
        'nr'  : child.pk,
        'user': child.created_by_str,
        'date': child.created
      })
  else:
    children_data = None
  
  
  context = {
    'elem': 5,
    'result': res,
    
    'refresh': refresh, #false or time in sec to refresh the page for fetching new images
    
    'lensdata': ldata,

    'print_result_items': [
      ('Id', res.pk),
      ('User', res.created_by_str),
      ('Pixel Radius', res.pixrad),
      ('Nr of models', res.n_models)
    ],
    
    'print_lensdata_items': lensdataitems,
             
    'images': {
      'lens'       : lensimg,
      'input'      : file_inp,
      'contour'    : file_1,
      'synthetic'  : file_3,
      'mass_dist'  : file_2,
      'mass_encl'  : file_4,
      'no_img_txt' : 'image not available'#refreshing image, please wait for reload'#<br/>esimated time: 1 minute'
    },
             
    'links': {
       'next' : children_data,#[{'nr': '005', 'user': 'aa'},{'nr': 'b', 'user': 'bb'},{'nr': 'c', 'user': 'cc'}],#[None],
       'prev' : parent_data,
       'fork' : '/?rid='+str(result_id), 
       'new'  : '/?mid='+str(res.lens_data_obj.pk)
    },
             
    'files': [    # tuple (download filename, [data]url)
      ('Model JSON Object', '%06i.json'%result_id, 'data:text/plain;base64,' + res.json_str.encode("base64")),
      ('Glass Config File', '%06i.config.gls'%result_id, file_gls),
      ('Glass State File (binary)', '%06i.state'%result_id, file_state),
      ('Glass Log File',    '%06i.log.txt'%result_id, file_log),
    ]
  
  }
  
  response = render(request, 'result.html', context)
  
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
      elif post['action'] == 'getResultData':
        resp = _getResultData(request, int(post['rid']))
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
    


def _getResultData(request, rid):
  print 'in getResultData', rid
  try:
    res = ModellingResult.objects.get(id=rid)
  except ModellingResult.DoesNotExist:
    raise Http404
  d = {
    'model_id': res.lens_data_obj.pk,
    'json_str': res.json_str
    }
  data = sjson.dumps(d)
  response = HttpResponse(data, content_type="application/json")
  return response



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
