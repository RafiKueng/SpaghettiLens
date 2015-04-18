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
#import random
import os
import hashlib
import base64

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect  # , Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.servers.basehttp import FileWrapper


#from couchdbkit.ext.django.loading import get_db
from couchdbkit import exceptions as CouchExceptions

from .utils import EvalAndSaveJSON

from .models import Model
from lenses.models import Lens

#from celery.result import AsyncResult

from .tasks import runGLASS

# Create your views here.

import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    os.chmod(path, 0777)  #TODO check what rights are really needed


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
    EASJobj = EvalAndSaveJSON(user_str = username,
                          data_obj= lens,
                          jsonStr = lmtmodel,
                          is_final= False)
                          
    obj = EASJobj.getDict()

    print "after eval and save"

    print '='*80
    print "EASJobj:"
    for k, v in EASJobj.__dict__['_'].items():
        print "%-16s : %s" % (k, v)
    print '='*80
        
    
    print '='*80
    print "parsed data obj:"
    for k, v in obj.items():
        print "%-16s : %s" % (k, v)
    print '='*80

    #model_id = "model_"+str(random.randint(100,999))

    m = hashlib.sha256()
    m.update(lens_id)
    m.update(lmtmodel)
    model_id = base64.b32encode(m.digest())[0:10]
    print 'model_id:', model_id

    now = datetime.datetime.utcnow()

    model = Model(
        lens_id = lens_id,
        parent = parent,
        
        created_by = username,
        created_at = now,
        comments = [[username, now, comment]],
        
        obj = obj,
        glass = {},
    
        task_id = None,
        rendered = False,
        isFinal = False,
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

    idd = model_id

    GLASSconfObj = model.obj
    config = {
        'model_id'   : model_id,
        'upload_host': settings.UPLOAD_HOST,
        'upload_user': settings.UPLOAD_USER,
        'upload_dest': os.path.join(settings.MEDIA_ROOT, 'spaghetti', idd[0:2], idd[2:])
    }
    
    mkdir_p(config['upload_dest'])
    
    task = runGLASS.delay(GLASSconfObj, config)
    status = task.status.lower()

#    print 'task:',task
#    print 'taskid:',task.id

    model.task_id = task.id
    model.save()
    
    return JsonResponse({'success': True, 'status': status, 'model_id': model_id, 'progress':{}})


def _getRenderingStatus(rq, model_id):
    
    try:
        model = Model.get(model_id)
    except CouchExceptions.ResourceNotFound as e:
        return JsonResponse({'success': False, 'error': 'Ressource not found (%s)' % e})
    
    # if alredy rendered
    if model.rendered:
        return JsonResponse({'success': True, 'status': 'done', 'progress': {}})
    # something odd, rendering not complete, but no task id (_startRendering was not called, should not happen)
    elif model.task_id == '':
        return _startRendering(rq, model_id)
        
        
        
    task = runGLASS.AsyncResult(model.task_id)
        
#    print 'task:',task
#    print 'taskid:',task.id
#    print "task.status:", task.status    
#    print "task.info:", task.info    
    
#    prog = {
#        'solutions': (6,600),
#        'models': (0,400),
#        'images': (0,4)
#    }

    prog = task.info
    
#    stat = "done" # done | pending
    stat = task.status.lower()
    
    if stat == "done":
        model.task_id = ""
        model.save()

    return JsonResponse({'success': True, 'status': stat, 'progress': prog})



def _testing(rq, bla):
    return HttpResponse("ok "+bla)










#
# This should not (yet) happen. Here I would need to start the image generation
# pipeline for files that don't exist.
# If the file exists in the database, it should be served by the webserver directly
#
def getMedia(rq, hash1, hash2, filename, ext):
    
    print '; '.join([hash1, hash2, filename, ext])
    return HttpResponse("ok "+ '; '.join([hash1, hash2, filename, ext]))



    idd = (hash1+hash2).lower() # can be full or reduced 3x3 form

    # someone gave a short id, which is not really supported
    if len(idd) == 8:
#        sid = hash1 + "-" + hash2
#        try:
#            idd = Lens.view('lenses/Lenses__by_name', key=sid).one(except_all=True)['id']
#        except CouchExceptions.MultipleResultsFound:
#            return HttpResponse("failed, multiple", status=404)
#        except CouchExceptions.NoResultFound:
#            return HttpResponse("failed, none", status=404)
#        except KeyError:
#            return HttpResponse("failed, key", status=404)
        return HttpResponse("failed, hashid wrong", status=404)

    # now, here I'm sure to have the full idd

    available_plots = [
        'kappa_plot',
        'arrival_plot',
        'srcdiff_plot',
        'srcdiff_plot_adv'
    ]
    
    redirect_filenames = {
        'img1': 'arrival_plot',
        'img2': 'kappa_plot',
        'img3': 'srcdiff_plot',
        'img3_ipol': 'srcdiff_plot_adv'
    }
    
    if filename in redirect_filenames.keys():
        newname = redirect_filenames[filename]
        return HttpResponsePermanentRedirect('/'.join(['','media', 'spaghetti', hash1, hash2, newname+'.'+ext]))
        
    if filename not in available_plots:
        return HttpResponse("failed, this plot is not available", status=404)

    # create the filenames in the storage
    #TODO: hardcoded paths are in here!!
    ddir = os.path.join(settings.MEDIA_ROOT, 'spaghetti', idd[:2], idd[2:])
    fname = '%s.%s' % (filename, ext)
    fpath = os.path.join(ddir, fname)
    
    # prepare the response already (will be sent if already exists or at end)
    # check if file already exists, then send it
    try:
        wrapper = FileWrapper(file(fpath))
        response = HttpResponse(wrapper, content_type='image/%s'%ext)
        response['Content-Length'] = os.path.getsize(fpath)
        #print "shortcut"
        return response    
    except IOError: # file does not exist: go on 
        pass 

    
    return HttpResponse("failed, server error, file not found", status=500)    








#def getMediaShort():





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
