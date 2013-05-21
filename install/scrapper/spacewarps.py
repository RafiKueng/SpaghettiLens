
import urllib2
import requests as rq
import re

try:
  from ModellerApp.models import BasicLensData, Catalog
  DEBUG=False
except:
  DEBUG=True
  print "running in debug mode: nothing will be added to database"

if not DEBUG:
  try:
  cat1 = Catalog.objects.get(name="SpaceWarps")
  except:
  cat1 = Catalog(
    name = "SpaceWarps",
    description = "selected SpaceWarps Lenses")
  cat1.save()

s = rq.Session()
imgid = raw_input("img id: ")
r1 = s.get("https://api.zooniverse.org/projects/spacewarp/talk/subjects/"+imgid)

json = r1.json()
url = json['location']['standard']
metaid = json['metadata']['id']

print "img id: %s | metaid: %s @ %s" % (imgid, metaid, url)
if not DEBUG and url:
  bld1 = BasicLensData(
    name = imgid,
    catalog = cat1,
    catalog_img_id = metaid,
    img_type = "CO",
    channel1_imgurl = url
  )
  bld1.save()
