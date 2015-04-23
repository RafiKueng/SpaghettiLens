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
  print 'post: ', post
  print post.dict()
  
  if x=='fetch':
    return _fetch(post['swid']);
  elif x=='createObj':
    print 'in api, create. post-data:', post.getlist('data[]')
    return _createObj(post.getlist('data[]'));
  else:
    print 'error in datasource spacewarps'
    return {}
  

  
def _fetch(swID):
  print 'in _fetch'

  s = rq.Session()
  r1 = s.get("https://api.zooniverse.org/projects/spacewarp/talk/subjects/"+swID)

  json = r1.json()
  url = json['location']['standard']
  metaid = json['metadata']['id']

  print "img id: %s | metaid: %s @ %s" % (swID, metaid, url)

  lenses = [{
    'id': swID,
    'metaid': metaid,
    'url': url,
    'pvurl': None,
    'metadata': json['metadata']
  }]
  
  s.close()
  return {'status': 'ok', 'list': lenses}
  
  

def _createObj(lenses):

  gIDs = []
  s = rq.Session()

  print 'lenses:', lenses
  for lensid in lenses:
    # check if obj already exists in db
    qs = LensData.objects.filter(
      datasource_id=lensid
    ).filter(
      datasource='spacewarps'
    )
    if qs.count()==1:
      print "object already in db:", qs[0].pk

      # retro update the pxScale
      ldo = qs[0]
      adddata = sjson.loads(ldo.add_data)
      adddata['orgPxScale'] = 0.187
      ldo.add_data = sjson.dumps(adddata)
      ldo.save()
      print 'retrofitting pxscale', ldo
      
      gID = qs[0].pk
      
    #if not, fetch new data
    else:
      r1 = s.get("https://api.zooniverse.org/projects/spacewarp/talk/subjects/"+lensid)

      json = r1.json()
      
      url = json['location']['standard']
      pvurl = json['location']['thumbnail']
      metaid = json['metadata']['id']
      id2 = json['id']
      
      print "creating obj:", lensid, metaid, id2, url
      
      ld = LensData(
        name=lensid,
        
        datasource = 'spacewarps',
        datasource_id = lensid,
        
        #created_by_str = user,
        
        img_data = sjson.dumps({'url':url, 'preview':pvurl}),
        add_data = sjson.dumps({
          'metaid': metaid,
          'id2': id2,
          'orgPxScale': 0.187 #http://www.cfht.hawaii.edu/Instruments/Imaging/Megacam/index.html
        })
      )
      ld.save()
      gID = ld.pk
    gIDs.append(gID)
  return gIDs
