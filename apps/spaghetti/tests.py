from django.test import TestCase
from django.core.urlresolvers import reverse

from pprint import pprint




class ApiTests(TestCase):
    
    def _post(self, data = {}):
        return self.client.post(reverse('spaghetti:api'), data=data)
        
        
    def assert200(self, response):
        self.assertEqual(response.status_code, 200)

    def assert400(self, response):
        self.assertEqual(response.status_code, 400)

    def assert404(self, response):
        self.assertEqual(response.status_code, 404)
        
        
    
    
    
    def test_if_api_reponding_to_get(self):
        response = self.client.get(reverse('spaghetti:api'))
        self.assertContains(response, "GET requests not supported, use POST", status_code=400)
        

    def test_if_api_reponding_to_empty_post(self):
        response = self._post()
        self.assert400(response)
        self.assertJSONEqual(response.content, {'status':"FAILED", 'error': "no_arguments"})
    
    
    
    def test_incomplete_post(self):
        response = self._post({'just':'something'})
        self.assert400(response)
        self.assertJSONEqual(response.content, {'status':"FAILED", 'error':'no_action_key'})

    def test_wrong_action(self):
        response = self._post({'action':'non_sense'})
        self.assert400(response)
        self.assertJSONEqual(response.content, {'status':"FAILED", 'error': "invalid_action"})
        
    def test_getInitData(self):
        response = self._post({'action':'GET_DATASOURCES'})
        self.assert200(response)
        self.assertJSONEqual(response.content, {'status':"SUCCESS"})
        
    def test_option_preflight(self):
        response = self.client.options(reverse('spaghetti:api'))
        #pprint(response.content)
        self.assertEqual(response['Access-Control-Allow-Origin'], "*")
        self.assertTrue("GET"     in response['Access-Control-Allow-Methods'])
        self.assertTrue("POST"    in response['Access-Control-Allow-Methods'])
        self.assertTrue("OPTIONS" in response['Access-Control-Allow-Methods'])
        self.assertTrue(int(response['Access-Control-Max-Age'])>60)
        
        
        
