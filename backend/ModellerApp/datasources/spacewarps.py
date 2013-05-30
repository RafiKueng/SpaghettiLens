from ModellerApp.models import LensData
from django.utils import simplejson as sjson

import urllib2
from bs4 import BeautifulSoup
import requests as rq
import re
import time

__id = "spacewarps"

def getID():
  return __id
  
def getDesc():
  return "SpaceWarps"
  
def getDialog():
  html = """
<div id='sw_loginfield'>
  <p>Image / Collection ID:<br/>
  <label for="swid">ID:</label>
  <input type="text" name="swid" id="swid" class="text ui-widget-content ui-corner-all" />
  <br/>
  <button id='sw_fetch'>Fetch Data</button>
  </p>
</div>
<div id='sw_selection_field'>
</div>
"""

  title = "SpaceWarps Image / Collection Access"

  return {'id':__id, 'html':html, 'title': title}
  
  
def api(post):
  
  x=post['do']
  #print 'post: ', post
  
  if x=='fetch':
    return _fetch(post['swid']);
  elif x=='createObj':
    #print 'in api, create. post-data:', post.getlist('data[]')
    return _createObj(post['user'], post['psw'], post.getlist('data[]'));
  else:
    print 'error in datasource masterlens'
    return {}
  

  
def _fetch(swID):
  print 'in _fetch'

  s = rq.Session()
  r1 = s.get("https://api.zooniverse.org/projects/spacewarp/talk/subjects/"+swID)

  json = r1.json()
  url = json['location']['standard']
  metaid = json['metadata']['id']

  print "img id: %s | metaid: %s @ %s" % (imgid, metaid, url)

  lenses = [{
    'id': swID,
    'metaid': metaid,
    'url': url,
    'pvurl': None,
    'metadata': json['metadata']
  }]
  
  return {'status': 'ok', 'list': lenses}
  
  

def _createObj(lenses):

  gIDs = []

  print 'iddata', lenses
  for lens in lenses:
    print lens
  
    # check if obj already exists in db
    qs = LensData.objects.filter(
      datasource_id=lens['id']
    ).filter(
      datasource='spacewarps'
    )
    if qs.count()==1:
      print "object already in db:", qs[0].pk
      gID = qs[0].pk

    #if not, fetch new data
    else:
      print idnr, name, z_lens, z_src, url
      
      ld = LensData(
        name=name,
        
        datasource = 'spacewarps',
        datasource_id = lens['id'],
        
        img_data = sjson.dumps({'url':lens['url']}),
        add_data = sjson.dumps(lens['metadata'])
      )
      ld.save()
      gID = ld.pk
    gIDs.append(gID)
  return gIDs
