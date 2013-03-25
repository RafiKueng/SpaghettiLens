
import urllib2
from bs4 import BeautifulSoup
import requests as rq
import re

try:
  from ModellerApp.models import BasicLensData, Catalog
except:
  DEBUG=True
  print "running in debug mode: nothing will be added to database"

if not DEBUG:
  cat1 = Catalog(
    name = "Masterlens",
    description = "Masterlens Database")
  cat1.save()

s = rq.Session()
r1 = s.get("http://admin.masterlens.org/member.php")
user = raw_input("username: ")
pw = raw_input("username: ")

data = {'ipaddress':'217.162.244.23', 'member':'Login', 'password': pw, 'username':user}
r2 = s.post("http://admin.masterlens.org/member.php", data = data)
r3 = s.get("http://admin.masterlens.org/search.php?")

s1 = BeautifulSoup(r3.text, "html5lib")
s2 = s1.find(id="message-listing")
s3 = s2.table.tbody
trows = s3.find_all('tr')

for i, row in enumerate(trows):
  c1 = row.find_all('td')
  c2 = row.find_all('th')
  id = int(re.search('\(\d+\)',str(c1[1])).group()[1:-1])
  fimg = s.get("http://admin.masterlens.org/graphic.php?lensID=%i&type=0&" % id)
  s11 = BeautifulSoup(fimg.text, "html5lib")
  s12 = s11.body.table.tbody.find('img')
  url = s12.attrs['src']
  if url[-11:]=='waiting.png':
    url = None
  else:
    url = 'http://admin.masterlens.org' + url[1:]

  yr = c1[0].text
  name = c1[1].a.text
  
  try:
    z_lens = float(re.search("^\d+.\d*", c1[6].text).group())
  except:
    z_lens = ''
  try:
    z_src = float(re.search("^\d+.\d*", c1[7].text).group())
  except:
    z_src = ''
    
  print "#%03i: id:%03i %s, %s, (zl: %s; zs: %s) @ %s" % (i, id, name, yr, z_lens, z_src, url)

  if not DEBUG and url:
    bld1 = BasicLensData(
      name = name,
      catalog = cat1,
      catalog_img_id = id,
      img_type = "CO",
      channel1_imgurl = url
    )
    if z_lens:
      bld1.z_lens = z_lens
    if z_src:
      bld1.z_src = z_src
    bld1.save()