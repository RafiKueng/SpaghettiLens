# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

import datetime as DT


from LensesDB_app.models import Datasource, Lens


class LensesDB_datasource_ModelTests(TestCase):
    
    def test_model_datasource(self):
        ds = Datasource(
                name='somename',
                provides=['a', 'b']
                )
        
        self.assertEqual('somename', ds.name)
        self.assertEqual(ds.provides[0], 'a')
        self.assertEqual(ds.provides[1], 'b')
        
        
class LensesDB_lens_ModelTests(TestCase):

    def test_model_lens(self):
        d = {'a':3, 'b':4}
        earlier = DT.datetime.utcnow()

        L = Lens(
                names=['a','b'],
                scidata=d,
                imgdata=d,
                metadata=d,
                )
        
        self.assertGreater(L.created_at, earlier)
        self.assertEqual(L.names[1], 'b')
        self.assertEqual(L.imgdata['b'], 4)
        


class LensesDB_Api_Basic_ViewTests(TestCase):
    
    def setUp(self):
        self.url = reverse('LensesDB:api')
    
    def test_no_args(self):
        resp = self.client.get(self.url)
        respjson = resp.json()
        
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(respjson['success'])
        self.assertIsNotNone(respjson['error'])
        
    def test_no_action(self):
        resp = self.client.get(self.url, {
                'something': True
                })
        respjson = resp.json()
        
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(respjson['success'])
        self.assertIsNotNone(respjson['error'])

    def test_wrong_action(self):
        resp = self.client.get(self.url, {
                'action': 'nonsense'
                })
        respjson = resp.json()
        
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(respjson['success'])
        self.assertIsNotNone(respjson['error'])
        
    def test_missing_param(self):
        resp = self.client.get(self.url, {
                'action': 'fetch_lens',
                'lensname': 'Something' # but "datasource" is missing
                })
        respjson = resp.json()
        
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(respjson['success'])
        self.assertIsNotNone(respjson['error'])
        
    def test_options_request(self):
        resp = self.client.options(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
                resp._headers['access-control-allow-origin'][1],
                '*')
        self.assertEqual(
                resp._headers['access-control-max-age'][1],
                '180')
        self.assertIn( "POST",
                resp._headers['access-control-allow-methods'][1])
        self.assertIn( "GET",
                resp._headers['access-control-allow-methods'][1])
        

class LensesDB_Api_GetListOfLenses_ViewTests(TestCase):
    
    def setUp(self):
        d = {'a':3, 'b':4}

        L0 = Lens(names=['aaaa','bbbb'],
                scidata=d, imgdata=d, metadata=d)
        L1 = Lens(names=['cccc','dddd', 'eeee'],
                scidata=d, imgdata=d, metadata=d)
        L2 = Lens(names=['ffff'],
                scidata=d, imgdata=d, metadata=d)

        self.Ls = [L0, L1, L2]
        self.url = reverse('LensesDB:api')

        # [L.save() for L in self.Ls]
        
    def test_simple(self):
        self.assertTrue('bbbb' in self.Ls[0].names)

        

#class LensesDB_GetGui_Tests(TestCase):
#    
#    def test_basic_response(self):
#        response = self.client.get(reverse('LensesDB:getGui'))
#        self.assertEqual(response.status_code, 200)

        