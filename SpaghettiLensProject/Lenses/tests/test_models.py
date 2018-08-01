#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 18:34:12 2018

@author: rafik
"""
from __future__ import unicode_literals, print_function

import io

from django.test import TestCase
from django.core.files.base import ContentFile

from Lenses.models import Lens
import json


class LensTestCase(TestCase):
    
    def setUp(self):
        
#        img = io.BytesIO(b'PNG a simple dummy image file')
        img = ContentFile('PNG a simple dummy image file')
        scidata = {
            'redshift_lens': 2,
            'redshift_source': 1
        }
        
        l = Lens.objects.create(
            names=['testfile', 'dummyfile'],
            origin_uri = '[uploaded]',
            file = img,
        )
        
#        l.file.save('blah', img)
        
        l.set_scidata(scidata)
        l.save()
        
        self.lens = l.hash

        
    def test_Lens_exists(self):
        
        assert len(Lens.objects.all()) == 1
        print(self.lens)
        assert self.lens.hash

        