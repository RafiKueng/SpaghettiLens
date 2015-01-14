# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 17:39:19 2014

@author: rafik
"""
from __future__ import absolute_import

import time
import pprint
import json

# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # , Http404
from django.views.decorators.csrf import csrf_exempt

#from celery.result import AsyncResult

from .tasks import add

# Create your views here.

@csrf_exempt
def celery_test(request):
    x=int(request.GET['x'])
    y=int(request.GET['y'])

    task = add.delay(x,y)

    pprint.pprint(task.__dict__)
    
    res1 = task.info
    print '1', task.status

    time.sleep(1)    
    
    res2 = task.info
    print 2, task.status

    time.sleep(1)    
    
    res3 = task.info
    print 3, task.status
    
    s0 = task.get()
    res4 = task.info
    print 4, task.status
    
    txt  = "we're testing\n"
    txt += "%s + %s = %s\n" % (x,y,s0)
    txt += "%s; %s; %s; %s \n" % (res1, res2, res3, res4)
    return HttpResponse(txt)


@csrf_exempt
def couch_test(request):
    txt = ''
    return HttpResponse(txt)



@csrf_exempt
def api(request):

    if request.method == 'GET':
        return HttpResponse("GET requests not supported, use POST", status=400)

    elif request.method == 'POST':

        if len(request.POST) == 0:
            return JsonResponse({'status': "FAILED", 'error': "no_arguments"}, status=400)

        elif 'action' not in request.POST.keys():
            return JsonResponse({'status': "FAILED", 'error': "no_action_key"}, status=400)

        action = request.POST['action']

        if action == 'bla':
            pass

        elif action == 'GET_DATASOURCES':
            return JsonResponse({'status': "SUCCESS"}, status=200)

        # Enter more

        else:
            return JsonResponse({'status': "FAILED", 'error': "invalid_action"}, status=400)

    elif request.method == 'OPTIONS':
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
        response['Access-Control-Allow-Headers'] = "x-requested-with, x-requested-by"
        response['Access-Control-Max-Age'] = "180"
        return response


    else:
        return HttpResponse("only POST (and OPTIONS) interface allowed", status=400)


#
#
#
# END
