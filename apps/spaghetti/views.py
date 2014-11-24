# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 17:39:19 2014

@author: rafik
"""


#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse#, Http404
from django.views.decorators.csrf import csrf_exempt



# Create your views here.


@csrf_exempt
def api(request):

    if request.method == 'GET':
        return HttpResponse("GET requests not supported, use POST", status=400)

    elif request.method == 'POST':

        if len(request.POST) == 0:
            return JsonResponse({'status':"FAILED", 'error': "no_arguments"}, status=400)

        elif not 'action' in request.POST.keys():
            return JsonResponse({'status':"FAILED", 'error':"no_action_key"}, status=400)


        action = request.POST['action']

        if action == 'bla':
            pass

        elif action == 'GET_DATASOURCES':
            return JsonResponse({'status':"SUCCESS"}, status=200)




        else:
            return JsonResponse({'status':"FAILED", 'error':"invalid_action"}, status=400)

    elif request.method == 'OPTIONS':
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
        response['Access-Control-Allow-Headers'] = "x-requested-with, x-requested-by"
        response['Access-Control-Max-Age'] = "180"
        return response


    else:
        return HttpResponse("only POST (and OPTIONS) interface allowed", status=400)

