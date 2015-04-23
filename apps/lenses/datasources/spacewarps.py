# -*- coding: utf-8 -*-
"""

ASW0007k4r

Created on Thu Jan 15 18:38:44 2015
@author: rafik
"""

import requests
import re
from PIL import Image
from StringIO import StringIO
import hashlib

from _types import DATATYPES, SUBTYPES

def validate(txt):
    '''Guess if name could be valid
    
    This tries to guess whether this could be a valid name for this datasource
    Should be really quick, gets hitten alot. No requests!
    '''

    if txt.startswith('ASW') and len(txt)==10:
        return True
    else:
        return False
        
        
        
def fetch(lensname):
    '''gets the image and its data
    
    if failed:
        return (False, 'error description')
    if successful:
        return (True, data, metadata, hash)
    #DONE note: maybe loading the image to ram and passing it around
                isn't a good idea in case of huge fits files...
    hash ist just some hash (sha256) of something (the image) used for id
    generation (so that the same image results in the same id)
    
    note: this has a filesize limit!
    '''

    max_file_size = 10*2**20 # 10 MiB
    min_file_size = 10*2**10 # 10 KiB
    
    if not validate(lensname):
        return (False, 'pattern failed')

    s = requests.Session()

    try:
        resp = s.get("https://api.zooniverse.org/projects/spacewarp/talk/subjects/"+lensname)
    except:
        return (False, 'remote database not available')
    if resp.status_code >= 400 or len(resp.text) ==0:
        return (False, 'remote database returned 404 or nothing')
        
    json = resp.json()

    # check if the provided link is valid and/or maybe redirect
    try:
        resp2 = s.get(json['location']['standard'])
    except:
        return (False, 'resource / img not available')

    if int(resp2.headers['content-length']) <= min_file_size: #images should be at least 10kiB to be valid
        return (False, 'resource / img too small to be an image')
    elif int(resp2.headers['content-length']) > max_file_size:
        return (False, 'resource / img too big')
        
    
    urls = []
    for r in [resp2] + resp2.history:
        urls.append(r.url)
    
    try:
        i = Image.open(StringIO(resp2.content))
    except:
        return (False, 'not an valid image')
        
    #gereate image hash
    ihash = hashlib.sha256(resp2.content).hexdigest()

    imgdata = [(DATATYPES.COMPOSITE_PIXEL_IMAGE, {
        SUBTYPES.COMPOSITE_PIXEL_IMAGE.DEFAULT : {
            'urls'  : urls,
            'scale' : [0.187, 'arcsec/pixel'],
            'format': i.format,
            'size'  : list(i.size+('pixel',)),
            'hash'  : ihash,
    }})]
        
    wanted_keys = ['activated_at','classification_count','created_at',
                   'group_id','id','location','metadata','project_id',
                   'random','state','tags','updated_at','workflow_ids',
                   'zooniverse_id']

    metadata = {k: json[k] for k in set(wanted_keys) & set(json.keys())} # only gets the wanted_keys from json
    
    # fetch additional stuff
    # claude added SDSS ids for many items:
    sdss_obj   = re.findall(r'SDSS(\w\d{6}\.\d{2}-\d{6}\.\d)', resp.text)
    sdss_objid = re.findall(r'\d{19}', resp.text)
    #print resp.text
    #print sdss_obj, sdss_objid
    if len(sdss_obj)>0:
        metadata['SDSS_obj'] = sdss_obj[0]
        metadata['SDSS_objid'] = sdss_objid[0]
        
    # spaghettilens doesn't provide any scientific data
    scidata = {}
    
    #print data
    #print metadata
    return (True, scidata, imgdata, metadata, ihash)

