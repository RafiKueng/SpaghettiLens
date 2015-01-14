from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # , Http404
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def getGui(request):
    
    return HttpResponse("parent.Response_OK()", mimetype="application/x-javascript")


@csrf_exempt
def api(request):
    
    return HttpResponse("")
   