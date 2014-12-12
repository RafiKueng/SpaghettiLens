# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:01:43 2014

@author: rafik
"""
from __future__ import absolute_import


import sys
#import os

import unittest as ut

from fabric.api import run, env, cd, local, hide
#from .fab_tools import GetOutOfLoop
#from .fab_tools import inform, warnn, lmanagepy, errorr, confirm, choose

from .settings import settings as _S




_E = env






#
#class test_server_setup(ut.TestCase):
#    """Test if server setup is ready
#    
#    This runs locally on dev server and checks if remote server is available
#    and basic stuff is set up.
#    All other test will be run locally on the live server..
#    """
#    
#    def setUp(self):
#        pass
#    def tearDown(self):
#        pass
#    
#    def test_dirs_existing(self):
#        pass



class ServerDjangoTestCase(ut.TestCase):
    """
    
    runns locally on server
    """
    

    def setUp(self):
        self.py_req_version = (2,7)
        self.py_max_version = (3,0) # dont allow python3
        self.django_req_ver = (1,7)
        
        
    def local(self, cmd):
        #print 'hiding'
        with hide('running', 'output'):
            return local(cmd, capture=True)
        
        
    
    def test_01_python_version(self):
        self.assertGreaterEqual(sys.version_info, self.py_req_version)
        self.assertLess(sys.version_info, self.py_max_version)
        
        
    def test_02_django_version(self):
        import django as d
        self.assertGreaterEqual(d.VERSION, self.django_req_ver)
        cmd = self.local("apps/manage.py --version")
        self.assertTrue(cmd.succeeded)
        self.assertGreaterEqual(tuple(map(int, cmd.stdout.split('.'))), self.django_req_ver)




class ServerRedisTestCase(ut.TestCase):
    
    def setUp(self):
        import redis
        try:
            self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        except:
            raise
        
    def test_01_connection(self):
        try:
            self.r.info()
        except ConnectionError:  #TODO CONTINUE: ConnectionError is not defined, maybe import?
            self.fail("Connection to redis failed")
        except:
            raise
            
        
    def test_02_save_and_retrieve(self):
        val = 'blablabla'
        self.r.set('foo', val)
        self.assertEqual(self.r.get('foo'), val)
    
    
        
    



def runTestSuite_ServerAll():
    tcs = [
        ServerDjangoTestCase,
        ServerRedisTestCase,  
        ]
    suites = []
    
    for t in tcs:
        tl = ut.TestLoader()
        tl.sortTestMethodsUsing = None
        suites.append(tl.loadTestsFromTestCase(t))
    suite = ut.TestSuite(suites)
    ut.TextTestRunner(verbosity=2).run(suite)    



def runTestSuite_ServerDjango():
    tl = ut.TestLoader()
    tl.sortTestMethodsUsing = None
    suite1 = tl.loadTestsFromTestCase(ServerDjangoTestCase)
    suite = ut.TestSuite([suite1])
    ut.TextTestRunner(verbosity=2).run(suite)    


def runTestSuite_ServerRedis():
    tl = ut.TestLoader()
    tl.sortTestMethodsUsing = None
    suite1 = tl.loadTestsFromTestCase(ServerDjangoTestCase)
    suite = ut.TestSuite([suite1])
    ut.TextTestRunner(verbosity=2).run(suite)    


#      
#class LocalSourceCodeTestCase(ut.TestCase):
#    '''Tests the local sourcecode (static analysis, pylint)'''
#
#    def setUp(self):
#        pass
#    def test_bla(self):
#        pass
#
#
#
#
#def runSuite_DjangoUnittest():
#    suite1 = ut.TestLoader().loadTestsFromTestCase(LocalSourceCodeTestCase)
##    suite2 = ut.TestLoader().loadTestsFromTestCase(LocalSourceCodeTestCase)
##    suite3 = ut.TestLoader().loadTestsFromTestCase(LocalSourceCodeTestCase)
#
#    #return ut.TestSuite([suite1, suite2])
#    suite = ut.TestSuite([suite1])
#    ut.TextTestRunner(verbosity=0).run(suite)
    



if __name__ == '__main__':
    ut.main()