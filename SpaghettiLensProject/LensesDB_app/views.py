# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from __future__ import absolute_import


import os
import hashlib
import requests

from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect #, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
# from django.core.servers.basehttp import FileWrapper
from django.conf import settings

from models import Datasource, Lens
#from . import datasources as pyDatasources



@csrf_exempt
def getGui(request):    
    return HttpResponse("parent.Response_OK()", mimetype="application/x-javascript")


def getApiDef():
#  'api_call: (_apiCallback, [req_keyword0, ...])' 
#   -> GET /api_call?req_keyword=val0&req...   -> python _apiCallback(request)
    return {
#        'get_datasource_dialog': _getDataSourceDialog,
        'get_list_of_lenses':     (_getListOfLenses,
                                   ['term']),
        'get_select_lens_dialog': (_getSelectLensDialog,
                                   []),
        'check_lensname_pattern': (_checkLensNamePatternAgainstDatasource,
                                   ['lensname', 'datasource']),
        'fetch_lens':             (_fetchRemoteLens,
                                   ['lensname', 'datasource']),
        'get_lens_data':          (_getLensData,
                                   ['lens_id']),
    }


@csrf_exempt
def api(request):

    if request.method == 'GET':
        if len(request.GET) == 0:
            return JsonResponse(
                    {'success': False, 'error': "no arguments"},
                    status=400
                    )

        elif 'action' not in request.GET.keys():
            return JsonResponse(
                    {'success': False, 'error': "no action defined"},
                    status=400
                    )

        action = request.GET['action']
        APIDEF = getApiDef()
        
        if action in APIDEF.keys():
            fn, kwargs = APIDEF[action]
            for kwarg in kwargs:
                if request.GET.get(kwarg) is None:
                    return JsonResponse(
                            {'success': False, 'error': "get_param_missing", 'details':kwarg},
                            status=400
                            )
            return fn(request)
            
        else:
            return JsonResponse(
                    {'success': False, 'error': "invalid_action"},
                    status=400
                    )
            
    elif request.method == 'OPTIONS':
        response = HttpResponse("")
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS"
        response['Access-Control-Allow-Headers'] = "x-requested-with, x-requested-by"
        response['Access-Control-Max-Age'] = "180"
        return response

    else:
        return HttpResponse("only GET (and OPTIONS) interface allowed", status=400)

    
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
    #lyst = [lens['key'] for lens in lenses if term in lens['key']]
    lyst = [{'label':lens['key'], 'value': lens['id'], 'url':'bbla'} for lens in lenses if term in lens['key']]
    
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
        
    _, scidata, imgdata, metadata, hhash = rvals
    
    nimgdata = {}
    
    for typ, dat in imgdata:
        nimgdata[typ] = {dsid: dat}

    m = hashlib.sha256()
    m.update(dsid)
    m.update(lensname)
    m.update(hhash)
    
    l_id = m.hexdigest()
    
    short_id = l_id[0:9]
    short_id = '-'.join([short_id[i:i+3] for i in [0,3,6]])
    # this is a human readable EnoughUniqueId.. hopefully
    # NOTE: probability of collision:
    # http://stackoverflow.com/questions/19962424/probability-of-collision-with-truncated-sha-256-hash    
    # 8 hex chars = 32bits (4bit / hexchar)
    # 2**(8*4/2) = 65536 entries, so many entries, then collisions start to happen
    # 2**(10*4/2) =~ 1mio entries using 10 hex chars
    # 2**(9*4/2) =~ 250'000 entries using 9 hex chars
    
    lens = Lens(
        names = [short_id, lensname],
        scidata = scidata,
        imgdata = nimgdata,
        metadata = metadata
    )
    
    lens._id = l_id

    try:
        lens.save()
    except CouchExceptions.ResourceConflict:
        return JsonResponse({'success': False, 'error': 'Ressource already present ()'})
    
    
#    keys = ['successful', 'lensid', 'lensname']        
#    data = dict(zip(keys, rvals))
#    return JsonResponse({'status': "SUCCESS", 'data': data})
    return JsonResponse({'success': True, 'data': {'lens_id':l_id}})


def _getLensData(rq):
    
    lens_id = rq.GET['lens_id']
    
    try:
        lens = Lens.get(lens_id)
    except CouchExceptions.ResourceNotFound as e:
        return JsonResponse({'success': False, 'error': 'Ressource not found (%s)' % e})
    
    return JsonResponse({'success': True, 'data': lens.to_json()})





################################################################################
### MEDIA QUERRIES                                                           ###
################################################################################


def getMedia(request, hash1, hash2, datatype, datasource, subtype, ext):
    #print hash1, hash2, datatype, datasource, subtype, ext
    #print request.path
   
    idd = (hash1+hash2).lower() # can be full or reduced 3x3 form

    if len(idd) == 9:
        sid = '-'.join([idd[i:i+3] for i in [0,3,6]])
        try:
            idd = Lens.view('lenses/Lenses__by_name', key=sid).one(except_all=True)['id']
        except CouchExceptions.MultipleResultsFound:
            return HttpResponse("failed, multiple", status=404)
        except CouchExceptions.NoResultFound:
            return HttpResponse("failed, none", status=404)
        except KeyError:
            return HttpResponse("failed, key", status=404)

    # now, here I'm sure to have the full idd

    # create the filenames in the storage
    #TODO: hardcoded paths are in here!!
    ddir = os.path.join(settings.MEDIA_ROOT, 'lenses', idd[:2], idd[2:])
    fname = '%s-%s-%s.%s' % (datatype, datasource, subtype, ext)
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
        
    try:
        l = Lens.get(idd)
    except CouchExceptions.ResourceNotFound:
        return HttpResponse("failed, no id found", status=404)
    
    try:
        d = l['imgdata'][datatype][datasource][subtype]
        urls = d['urls']
        pext = d['format']
    except KeyError:
        return HttpResponse("failed, lens data wrong", status=404)
    
    # uups, got wrong extension...
    if not ext.lower() == pext.lower():
        return HttpResponsePermanentRedirect('/media/lenses/%s/%s/%s-%s-%s.%s' % (idd[:2], idd[2:], datatype, datasource, subtype, pext))

    if not os.path.exists(ddir):
        os.makedirs(ddir)
    
    # download the file first to the server
    # stream it to avoid loading the file into memory
    r = requests.get(urls[0], stream=True)
    if r.status_code == 200:
        with open(fpath, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    
    # then upload it to the client directly
    # http://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    # https://djangosnippets.org/snippets/365/
    #
    # I let django serve the files, so that the dev server works without an additional apache in front
    # This is slightly better than loading the whole file to memory. It is served in chunks.
    # (otherwise downloading a file of 1gb would make the server run out of ram quickly)
    #
    wrapper = FileWrapper(file(fpath))
    response = HttpResponse(wrapper, content_type='image/%s'%ext)
    response['Content-Length'] = os.path.getsize(fpath)
    return response


