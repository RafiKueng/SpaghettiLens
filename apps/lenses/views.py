from __future__ import absolute_import

import re

#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest  # , Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader

from .models import Datasource, Lens

from . import datasources as pyDatasources

# Create your views here.

@csrf_exempt
def getGui(request):
    
    return HttpResponse("parent.Response_OK()", mimetype="application/x-javascript")


def getApiDef():
#  'api_call: (_apiCallback, [req_keyword0, ...])' 
#   -> GET /api_call?req_keyword=val0&req...   -> python _apiCallback(request)
    return {
#        'get_datasource_dialog': _getDataSourceDialog,
        'get_list_of_lenses': (_getListOfLenses, ['term']),
        'get_select_lens_dialog': (_getSelectLensDialog, []),
        'check_lensname_pattern': (_checkLensNamePatternAgainstDatasource, ['lensname', 'datasource']),
        'fetch_lens': (_fetchRemoteLens, ['lensname', 'datasource']),
    }


@csrf_exempt
def api(request):

    
    if request.method == 'GET':
        if len(request.GET) == 0:
            return JsonResponse({'success': False, 'error': "no_arguments"})

        elif 'action' not in request.GET.keys():
            return JsonResponse({'success': False, 'error': "no_action_key"})

        action = request.GET['action']
        APIDEF = getApiDef()
        
        if action in APIDEF.keys():
            fn, kwargs = APIDEF[action]
            for kwarg in kwargs:
                if request.GET.get(kwarg) is None:
                    return JsonResponse({'success': False, 'error': "get_param_missing", 'details':kwarg})
            return fn(request)
            
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
        return HttpResponse("only GET (and OPTIONS) interface allowed. and this will be using json", status=400)





#def _getDataSourceDialog(request):
#
#    datasources = Datasource.view("lenses/Datasources")
#
#
##    htmltemplate = loader.get_template('lenses/select_datasource.html')
#    htmltemplate = loader.get_template('lenses/select_datasource.html')
#    htmltemplate = loader.get_template('lenses/select_datasource.html')
#
#    context = RequestContext(request, {
#        'datasources': datasources,
#    })
#
#    html  = htmltemplate.render(context)
#    jsobj = jstemplate.render(context)
#    
#    return JsonResponse({'status': "SUCCESS", 'html': html, 'jsobj': jsobj})
    
def _getSelectLensDialog(request):

    datasources = Datasource.view("lenses/Datasources")


#    htmltemplate = loader.get_template('lenses/select_datasource.html')
    htmltemplate = loader.get_template('lenses/select_lens.html')
    jstemplate = loader.get_template('lenses/select_lens.js')

    context = RequestContext(request, {
        'datasources': datasources,
    })

    html  = htmltemplate.render(context)
    jsobj = jstemplate.render(context)
    
    return JsonResponse({'success': True, 'html': html, 'jsobj': jsobj})
    
    
    
def _getListOfLenses(request):
    
    term = request.GET.get('term')
    if term is None:
        return JsonResponse({'success': False, 'error': "term_missing"}, status=400)
        
    lenses = Datasource.view("lenses/Lenses__by_name")
    
#    lyst = [{'label':lens['key'], 'value': lens['id']} for lens in lenses if term in lens['key']]
    lyst = [lens['key'] for lens in lenses if term in lens['key']]
    
    #regex = re.compile('.*('+term+').*')
    #lyst = [m.group(0) for l in lenses for m in [regex.search(l['key'])] if m]
    
    return JsonResponse({'success': True, 'data': lyst})
            
        
def _checkLensNamePatternAgainstDatasource(rq):
    ds = Datasource.get(rq.GET['datasource'])
    py_mod = ds['py_module_name']
    mod = pyDatasources.__dict__[py_mod]
    val = mod.validate
    r = val(rq.GET['lensname']) if val is not None else True
    
    return JsonResponse({'success': True, 'data': r})
        
        
def _fetchRemoteLens(rq):
    dsid = rq.GET['datasource']
    ds = Datasource.get(dsid)
    lensname = rq.GET['lensname']
    py_mod = ds['py_module_name']
    mod = pyDatasources.__dict__[py_mod]
    rvals = mod.fetch(lensname) # rvals = successful, lensid, lensname
    
    if rvals[0] == False:
        return JsonResponse({'success': False, 'error': rvals[1]})
        
    _, data, metadata, i = rvals
    
    ndata = {}
    
    for typ, dat in data:
        ndata[typ] = {dsid: dat}
    
    lens = Lens(
        names = [lensname],
        data = ndata,
        metadata = metadata
    )
    
    lens.save()
    
#    keys = ['successful', 'lensid', 'lensname']        
#    data = dict(zip(keys, rvals))
#    return JsonResponse({'status': "SUCCESS", 'data': data})
    return JsonResponse({'success': True, 'data': []})
        