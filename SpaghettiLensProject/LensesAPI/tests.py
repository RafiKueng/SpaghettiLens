# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse


import datetime as DT
import types
import inspect
import mongomock

from LensesAPI.models import Datasource, Lens
import LensesAPI.views


class LensesAPI_datasource_ModelTests(TestCase):

    def test_model_datasource(self):
        ds = Datasource(
            name='somename',
            provides=['a', 'b']
        )

        self.assertEqual('somename', ds.name)
        self.assertEqual(ds.provides[0], 'a')
        self.assertEqual(ds.provides[1], 'b')
        
        
class LensesAPI_lens_ModelTests(TestCase):

    def test_model_lens(self):
        
        d = {'a': 3, 'b': 4}
        earlier = DT.datetime.utcnow()

        L = Lens(
            names=['a', 'b'],
            scidata=d,
            imgdata=d,
            metadata=d,
        )
        
        self.assertGreater(L.created_at, earlier)
        self.assertEqual(L.names[1], 'b')
        self.assertEqual(L.imgdata['b'], 4)
        

class LensesAPI_getApiDef_Tests(TestCase):
    
    def setUp(self):
        pass
    
    def test_if_dict(self):
        d = LensesAPI.views.getApiDef()
        self.assertTrue(type(d) is dict)

    def test_return_dict(self):
        '''Tests the returned dictionary for consitency with the code'''
        d = LensesAPI.views.getApiDef()

        for ep, v in d.items():  # ep = endpoint
            self.assertEqual(len(v), 2)
            fn, params = v
            
            self.assertTrue(isinstance(ep, unicode))
            self.assertTrue(callable(fn))
            self.assertTrue(isinstance(fn, types.FunctionType))
            self.assertTrue(isinstance(params, list))
            
            l1 = len(inspect.getargspec(fn).args) - 1  # -1: They all get the 'request' argument first
            l2 = len(params)
            self.assertEqual(
                l1, l2,
                "Number of args of API function '{}' ({}) mismatches the API definition ({})".format(ep, l1, l2)
            )
            




class LensesAPI_Basic_ViewTests(TestCase):
    """Tests basic function of the api"""
    
    def setUp(self):
        self.url = reverse('LensesAPI:api')
    
# #############################################################################

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
            'lensname': 'Something'  # but "datasource" is missing
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
            '180'
        )
        self.assertIn(
            "POST",
            resp._headers['access-control-allow-methods'][1]
        )
        self.assertIn(
            "GET",
            resp._headers['access-control-allow-methods'][1]
        )
        

class LensesAPI_GetListOfLenses_ViewTests(TestCase):
    
    def setUp(self):
        
        d = {'a': 3, 'b': 4}

        L0 = Lens(names=['aaaa', 'bbbb'],
                  scidata=d, imgdata=d, metadata=d)
        
        L1 = Lens(names=['cccc', 'dddd', 'eeee'],
                  scidata=d, imgdata=d, metadata=d)
        
        L2 = Lens(names=['ffff'],
                  scidata=d, imgdata=d, metadata=d)

        self.Ls = [L0, L1, L2]
        self.url = reverse('LensesAPI:api')

        # [L.save() for L in self.Ls]
        
    def test_failure(self):
        resp = self.client.get(self.url) # missing 'term'
        self.assertEqual(resp.status_code, 400)
        
    def test_simple(self):
        self.assertTrue('bbbb' in self.Ls[0].names)


# class LensesDB_GetGui_Tests(TestCase):
#
#    def test_basic_response(self):
#        response = self.client.get(reverse('LensesAPI:getGui'))
#        self.assertEqual(response.status_code, 200)
