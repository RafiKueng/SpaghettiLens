# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 17:39:19 2014

@author: rafik
"""
from __future__ import absolute_import

#import time
#import pprint
#import json
import datetime
import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # , Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

#from couchdbkit.ext.django.loading import get_db
from couchdbkit import exceptions as CouchExceptions

from .utils import EvalAndSaveJSON

from .models import Model
from lenses.models import Lens

#from celery.result import AsyncResult

from .tasks import runGLASS

# Create your views here.




@csrf_exempt
def getIndex(request):
    context = {}
    return render(request, 'spaghetti/index.html', context)




def getApiDef():
#  'api_call: (_apiCallback, [req_keyword0, ...])' 
#   -> GET /api_call?req_keyword=val0&req...   -> python _apiCallback(request)
    return {
        'test':             (_testing, ['bla']),
        'save_model':       (_saveModel,
                             ['lmtmodel', 'lens_id', 'parent', 'username', 'comment']),
        'start_rendering':  (_startRendering,
                             ['model_id']),
        'get_rendering_status':  (_getRenderingStatus,
                             ['model_id']),
    }


@csrf_exempt
def api(request):

    #print request.GET, request.POST
    
    if request.method in ['GET', 'POST']:
        if len(request.GET) == 0 and len(request.POST) == 0:
            return JsonResponse({'success': False, 'error': "no_arguments"})

        elif 'action' not in request.GET.keys() and 'action' not in request.POST.keys():
            return JsonResponse({'success': False, 'error': "no_action_key"})

        action = request.GET.get('action', request.POST.get('action'))
        APIDEF = getApiDef()
        
        kwdict = {}
        if action in APIDEF.keys():
            fn, kwargs = APIDEF[action]
            for kwarg in kwargs:
                #print kwarg, request.GET.get(kwarg), request.POST.get(kwarg)
                if (request.GET.get(kwarg) is None) and (request.POST.get(kwarg) is None):
                    return JsonResponse({'success': False, 'error': "get_or_post_param_missing", 'details':kwarg})
                kwdict[kwarg] = request.GET.get(kwarg, request.POST.get(kwarg))
            return fn(request, **kwdict)
            
        else:
            return JsonResponse({'success': False, 'error': "invalid_action"})
            
    elif request.method == 'OPTIONS':
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
        response['Access-Control-Allow-Headers'] = "x-requested-with, x-requested-by"
        response['Access-Control-Max-Age'] = "180"
        return response

    else:
        return HttpResponse("only GET, POST and OPTIONS interface allowed. and this will be using json", status=400)












def _saveModel(rq, lmtmodel, lens_id, parent, username, comment):
    
    print "username:", username
    
    try:
        lens = Lens.get(lens_id)

    except CouchExceptions.ResourceNotFound as e:
        return JsonResponse({'success': False, 'error': 'Ressource not found (%s) The lens id doesnt exist!!' % e})
    

    print "eval and save"
    obj = EvalAndSaveJSON(user_str = username,
                          data_obj= lens,
                          jsonStr = lmtmodel,
                          is_final= False)

    print "after eval and save"
    print obj
    for k, v in obj.__dict__.items():
        print k, ': ', v


    model_id = "model_"+str(random.randint(100,999))
    print 'model_id:', model_id

    now = datetime.datetime.utcnow()

    model = Model(
        lens_id = lens_id,
        parent = parent,
        
        created_by = username,
        created_at = now,
        comments = [[username, now, comment]],
        
        obj = {},
        glass = {},
    
        task_id = None
    )
    
    model._id = model_id

    try:
        model.save()
    except CouchExceptions.ResourceConflict:
        return JsonResponse({'success': False, 'error': 'Ressource already present ()'})

    return JsonResponse({'success': True, 'model_id': model_id})
#    return HttpResponse("ok: "+'|'.join([lmtmodel, parent, username, comment]))








def _startRendering(rq, model_id):


    try:
        model = Model.get(model_id)
    except CouchExceptions.ResourceNotFound as e:
        return JsonResponse({'success': False, 'error': 'Ressource not found (%s)' % e})

    GLASSconfObj = {}
    config = {
        'upload_host': settings.UPLOAD_HOST,
        'upload_user': settings.UPLOAD_USER,
        'upload_dest': settings.MEDIA_ROOT
    }
    
    task = runGLASS.delay(GLASSconfObj, config)
    print 'task:',task
    print 'taskid:',task.id

    model.task_id = task.id
    model.save()
    
    return JsonResponse({'success': True, 'model_id': model_id})


def _getRenderingStatus(rq, model_id):
    
    try:
        model = Model.get(model_id)
    except CouchExceptions.ResourceNotFound as e:
        return JsonResponse({'success': False, 'error': 'Ressource not found (%s)' % e})
    
    task = runGLASS.AsyncResult(model.task_id)

    print 'task:',task
    print 'taskid:',task.id
    print "task.status:", task.status    
    print "task.info:", task.info    
    
    prog = {
        'solutions': (6,600),
        'models': (0,400),
        'images': (0,4)
    }

    prog = task.info
    
    stat = "done" # done | pending
    stat = task.status.lower()
    

    return JsonResponse({'success': True, 'status': stat, 'progress': prog})



def _testing(rq, bla):
    return HttpResponse("ok "+bla)











def getMedia(rq, hash1, hash2, filename, ext):
    print '; '.join([hash1, hash2, filename, ext])
    return HttpResponse("ok "+ '; '.join([hash1, hash2, filename, ext]))








#
#
#
#
#
#
#
#
#
#@csrf_exempt
#def celery_test(request):
#    x=int(request.GET['x'])
#    y=int(request.GET['y'])
#
#    task = add.delay(x,y)
#
#    pprint.pprint(task.__dict__)
#    
#    res1 = task.info
#    print '1', task.status
#
#    time.sleep(1)    
#    
#    res2 = task.info
#    print 2, task.status
#
#    time.sleep(1)    
#    
#    res3 = task.info
#    print 3, task.status
#    
#    s0 = task.get()
#    res4 = task.info
#    print 4, task.status
#    
#    txt  = "we're testing\n"
#    txt += "%s + %s = %s\n" % (x,y,s0)
#    txt += "%s; %s; %s; %s \n" % (res1, res2, res3, res4)
#    return HttpResponse(txt)
#
#
#@csrf_exempt
#def couch_test(request):
#    
#    tests = TestDoc.view("spaghetti/all")
#    
#    txt = 'Start:<br>'
#    for t in tests:
#        txt += str(t.blaa) + '<br>'
#        print t
#        
#    db = get_db('spaghetti')
#    
#    return HttpResponse(txt)
#
#
#
#@csrf_exempt
#def api(request):
#
#    if request.method == 'GET':
#        return HttpResponse("GET requests not supported, use POST", status=400)
#
#    elif request.method == 'POST':
#
#        if len(request.POST) == 0:
#            return JsonResponse({'status': "FAILED", 'error': "no_arguments"}, status=400)
#
#        elif 'action' not in request.POST.keys():
#            return JsonResponse({'status': "FAILED", 'error': "no_action_key"}, status=400)
#
#        action = request.POST['action']
#
#        if action == 'bla':
#            pass
#
#        elif action == 'GET_DATASOURCES':
#            return JsonResponse({'status': "SUCCESS"}, status=200)
#
#        # Enter more
#
#        else:
#            return JsonResponse({'status': "FAILED", 'error': "invalid_action"}, status=400)
#
#    elif request.method == 'OPTIONS':
#        response = HttpResponse("")
#        response['Access-Control-Allow-Origin'] = "*"
#        response['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
#        response['Access-Control-Allow-Headers'] = "x-requested-with, x-requested-by"
#        response['Access-Control-Max-Age'] = "180"
#        return response
#
#
#    else:
#        return HttpResponse("only POST (and OPTIONS) interface allowed", status=400)


#
#
#
# END
