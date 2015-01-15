


from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # , Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader

from .models import Datasource

# Create your views here.

@csrf_exempt
def getGui(request):
    
    return HttpResponse("parent.Response_OK()", mimetype="application/x-javascript")


def getApiDef():
    return {
        'get_datasource_dialog': _getDataSourceDialog
    }

@csrf_exempt
def api(request):

    
    if request.method == 'GET':
        if len(request.GET) == 0:
            return JsonResponse({'status': "FAILED", 'error': "no_arguments"}, status=400)

        elif 'action' not in request.GET.keys():
            return JsonResponse({'status': "FAILED", 'error': "no_action_key"}, status=400)

        action = request.GET['action']
        APIDEF = getApiDef()
        
        if action in APIDEF.keys():
            return APIDEF[action](request)
            
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
        return HttpResponse("only GET (and OPTIONS) interface allowed", status=400)





def _getDataSourceDialog(request):

    datasources = Datasource.view("lenses/Datasources")


    template = loader.get_template('lenses/select_datasource.html')

    context = RequestContext(request, {
        'datasources': datasources,
    })

    html = template.render(context)
    return JsonResponse({'status': "SUCCESS", 'html': html})