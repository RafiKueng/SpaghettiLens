
import urllib2
from bs4 import BeautifulSoup

from ModellerApp.models import BasicLensData, Catalog


cat1 = Catalog(
  name = "CASTLES original",
  description = "CASTLES Survey with original images")
cat2 = Catalog(
  name = "CASTLES cleaned",
  description = "CASTLES Survey with cleaned images")
cat1.save()
cat2.save()




soup = BeautifulSoup(urllib2.urlopen('http://www.cfa.harvard.edu/castles/').read())
tables = soup.find_all('table')

trows = tables[1].find_all('tr', {"align":"CENTER"})

for trow in trows:
  td=trow.find_all('td')

  cat_id = int(td[0].text)
  name = td[2].a.text
  url = td[2].a.get('href')
  z_src = td[4].text
  z_lens = td[5].text
  
  zi = [0.0, 0.0]
  for i, z in enumerate([z_src, z_lens]):
    if z=="":
      zi[i] = None
    if z[0] == "(":
      z = z[1:-1]
    if '/' in z:
      z = z.partition('/')[0] #throw away the rest..
    try:
      zi[i] = float(z)
    except ValueError:
      zi[i] = None
  z_src = zi[0]
  z_lens = zi[1]
  
  link = "http://www.cfa.harvard.edu/castles/" + url

  print "[%3i] %20s   (" % (cat_id, name), 
  print ("%.2f" % z_src) if z_src!=None else "-.--",
  print ("%.2f" % z_lens) if z_lens!=None else "-.--", " )"
  
  elem = BeautifulSoup(urllib2.urlopen(link).read())
  
  tmp = elem.find_all("p")[4]
  orig_imgurls = []
  orig_imgbands = []
  if tmp.text[1:9] == "Original":
    aimgs = tmp.find_all('a')
    
    for i, aimg in enumerate(aimgs):
      imgurl = "http://www.cfa.harvard.edu/castles/" + aimg['href'][3:]
      imgband = imgurl[-5:-4]
      print "  -> orig:", i, imgband, imgurl
      orig_imgurls.append(imgurl)
      orig_imgbands.append(imgband)
  else:
    print "  -> orig:", "[none found]"

  
    
  tmp = elem.find_all("p")[5]
  print "tmp", tmp
  clean_imgurls = []
  clean_imgbands = []
  if tmp.text[1:8] == "Cleaned":
    #print "in cleaned", 
    #print "tmp",tmp.contents[3]
    cc_aimgs = tmp.find_all('a')
    #print "ccaimgs", len(cc_aimgs), cc_aimgs
    for i, aimg in enumerate(cc_aimgs):
      imgurl = "http://www.cfa.harvard.edu/castles/" + aimg['href'][3:]
      imgband = imgurl[-7:-6]
      print "  -> cc:  ", i, imgband, imgurl
      clean_imgurls.append(imgurl)
      clean_imgbands.append(imgband)      
  else:
    print "  -> cc:  ", "[none found]"
  
  
  if len(orig_imgurls)>0:
    bld1 = BasicLensData(
      name = name,
      catalog = cat1,
      catalog_img_id = cat_id,
      z_lens = z_lens,
      z_source = z_src,
      img_type = "CO",
    )
    for i, url in enumerate(orig_imgurls):
      setattr(bld1, 'channel%i_imgurl'%i, url)
      setattr(bld1, 'channel%i_type'%i, orig_imgbands[i])
    bld1.save()

  if len(clean_imgurls)>0:
    bld1 = BasicLensData(
      name = name,
      catalog = cat2,
      catalog_img_id = cat_id,
      z_lens = z_lens,
      z_source = z_src,
      img_type = "CO",
    )
    for i, url in enumerate(clean_imgurls):
      setattr(bld1, 'channel%i_imgurl'%i, url)
      setattr(bld1, 'channel%i_type'%i, clean_imgbands[i])
    bld1.save()
    
    
