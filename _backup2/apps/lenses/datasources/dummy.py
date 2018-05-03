# -*- coding: utf-8 -*-
"""

ASW0007k4r

Created on Thu Jan 15 18:38:44 2015
@author: rafik
"""

import requests
from PIL import Image
from StringIO import StringIO


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
        return (True, data, metadata, PIL.Image)
    #TODO note: maybe loading the image to ram and passing it around
                isn't a good idea in case of huge fits files...
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
    for r in resp2.history + [resp2]:
        urls.append(r.url)
    
    try:
        i = Image.open(StringIO(r.content))
    except:
        return (False, 'not an valid image')

    data = [('COMPOSED_PIXEL_IMAGE', {
        'urls'  : urls,
        'scale' : (0.187, 'arcsec/pixel'),
        'format': i.format,
        'size'  : i.size,
    })]
        
    wanted_keys = ['activated_at','classification_count','created_at',
                   'group_id','id','location','metadata','project_id',
                   'random','state','tags','updated_at','workflow_ids',
                   'zooniverse_id']

    metadata = {k: json[k] for k in set(wanted_keys) & set(json.keys())} # only gets the wanted_keys from json
    
    print data
    print metadata
    return (True, data, metadata, i)

