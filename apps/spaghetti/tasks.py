# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 17:48:53 2015

@author: rafik
"""

from __future__ import absolute_import

import time

#from celery import shared_task
from _app.celery import app

#@shared_task
@app.task(bind=True)
def add(self, x, y):

    print 0
    
    time.sleep(1)    
    print 1

    if not self.request.called_directly:
        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 2})


    time.sleep(1)    
    print 2

    if not self.request.called_directly:
        self.update_state(state='PROGRESS', meta={'current': 1, 'total': 2})

    time.sleep(1)    
    print 3

    
    if not self.request.called_directly:
        self.update_state(state='PROGRESS', meta={'current': 2, 'total': 2})
        
    return x + y