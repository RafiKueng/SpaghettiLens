from ModellerApp.models import LensData
from django.utils import simplejson as sjson

import urllib2
from bs4 import BeautifulSoup
import requests as rq
import re
import time

__id = "masterlens"

def getID():
  return __id
  
def getDesc():
  return "Masterlens Database"
  
def getDialog():
  html = """
<div id='ml_loginfield'>
  <p>Login Data<br/>
  <label for="name">Username:</label>
  <input type="text" name="username" id="username" class="text ui-widget-content ui-corner-all" />
  <br/>
  <label for="psw">Password:</label>
  <input type="text" name="psw" id="psw" class="text ui-widget-content ui-corner-all" />
  <br/>
  <button id='ml_login'>Login</button>
  </p>
</div>
<div id='ml_selection_field'>
<p>test</p>
</div>
"""

  title = "Masterlens Database Access"

  return {'js':js, 'html':html, 'title': title}
  
  
def api(post):
  
  x=post['do']
  
  if x=='login':
    return _login(post['user'], post['psw']);
  elif x=='createObj':
    return _createObj(post['user'], post['psw'], post['data']);
  else:
    print 'error in datasource masterlens'
    return {}
  

cache = {
  'time': 0,
  'lenses': [],
}
  
def _login(user, psw):
  print 'in _login'

  #check if cache is still valid TODO: delete this after dev
  if time.time() - cache['time'] < 2 * 60 * 60 * 1000:
    return {'status': 'ok', 'list': cache['lenses'], 'detail': 'cached'}
  
  s = rq.Session()
  rq1 = s.get("http://admin.masterlens.org/member.php")

  data = {'member':'Login', 'password': psw, 'username':user}
  rq2 = s.post("http://admin.masterlens.org/member.php", data = data)

  soup1 = BeautifulSoup(rq2.text, "html5lib")
  
  #soup1.find('td', {'class':'red'})
  try:
    if not soup1.find('div', {'class':'galleryitems'}).find('h1').text == "Log in ":
      return {'status': 'error'}
  except:
    return {'status': 'error'}

  #check if cache is still valid
  if time.time() - cache['time'] < 2 * 60 * 60 * 1000:
    return {'status': 'ok', 'list': cache['lenses'], 'detail': 'cached'}

    
  rq3 = s.get("http://admin.masterlens.org/search.php?")
  soup2 = BeautifulSoup(rq3.text, "html5lib")
  
  trows = soup2.find(id="message-listing").table.tbody.find_all('tr')  
  
  lenses = []
  
  for i, row in enumerate(trows):
    c1 = row.find_all('td')
    c2 = row.find_all('th')
    id = int(re.search('\d+',c1[1].a.get('href')).group())
    name = c1[1].a.text
    preview_img_url = 'http://admin.masterlens.org' + row.img.attrs['src'][1:]
    #print id, name, preview_img_url
    lenses.append({'id': id, 'name': name, 'pvurl': preview_img_url})
  
  #update cache
  cache['time'] = time.time()
  cache['lenses'] = lenses
  
  
  return {'status': 'ok', 'list': lenses}
  
  

def _createObj(user, psw, iddata):

  s = rq.Session()
  rq1 = s.get("http://admin.masterlens.org/member.php")

  data = {'member':'Login', 'password': psw, 'username':user}
  rq2 = s.post("http://admin.masterlens.org/member.php", data = data)


  for idnr in iddata:
    print data, idnr
  
    # check if obj already exists in db
    qs = LensData.objects.filter(
      datasource_id__eq=idnr
    ).filter(
      datasource__eq='masterlens'
    )
    if qs.count()==1:
      pass;

    #if not, fetch new data
    else:
      data2 = {'inputaction': 'Search', 'lensID': idnr}
      rq3 = s.post("http://admin.masterlens.org/search.php?", data = data2)
      
      bs3 = BeautifulSoup(rq3.text, 'html5lib')
      trs = bs3.find_all('tr')
          
      vals = {}
      for tr in trs:
        ths = tr.find_all('th')
        for th in ths:
          td = th.findNextSibling('td')
          if (th is not None) and (td is not None) and (len(th.text)>0) and (len(td.text)>0):
            print '[%s]||[%s]' % (th.text, td.text)
            vals[th.text] = td.text

      fimg = s.get("http://admin.masterlens.org/graphic.php?lensID=%i&type=0&" % int(idnr))
      s11 = BeautifulSoup(fimg.text, "html5lib")
      s12 = s11.body.table.tbody.find('img')
      url = s12.attrs['src']
      if url[-11:]=='waiting.png':
        url = None
      else:
        url = 'http://admin.masterlens.org' + url[1:]
      try:
        z_lens = float(re.search("^\d+.\d*", vals['z_Lens']).group())
      except:
        z_lens = ''
      try:
        z_src = float(re.search("^\d+.\d*", vals['z_Source(s)']).group())
      except:
        z_src = ''
      name = vals['System Name']
      
      print idnr, name, z_lens, z_src, url
      
      ld = LensData(
        name=name,
        
        datasource = 'masterlens',
        datasource_id = 'idnr',
        
        img_data = sjson.dumps({'url':url}),
        add_data = sjson.dumps({
          'z_lens': z_lens,
          'z_src': z_src,
          'lens_grade': vals['Lens Grade'] 
        })
      )
      ld.save()
    
  s.close()

