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
    should be valid, due to the pip req file, but ceck anyways
    """
    

    def setUp(self):

        self.mod_vers = {
            'numpy':        [(1,9),(1,10)], #[>=(), <()]
            'scipy':        [(0,14),(0,15)],
            'matplotlib':   [(1,4),(1,5)],

            'django':       [(1,7), (1,8)],
            'Celery':       [(3,1,17), (3,2)],
            
        }
        
        self.py_req_version = (2,7)
        self.py_max_version = (3,0) # dont allow python3
        self.django_req_ver = (1,7)
        
        
    def local(self, cmd):
        #print 'hiding'
        with hide('running', 'output'):
            return local(cmd, capture=True)
        
        
    
    def test_01_python_version(self):
        '''test version of python'''
        self.assertGreaterEqual(sys.version_info, self.py_req_version)
        self.assertLess(sys.version_info, self.py_max_version)
        
        
    def test_managepy_version(self):
        '''test the local manage.py reported version'''
        
        cmd = self.local("python %s/manage.py --version" % _S.APPS.DIR)
        self.assertTrue(cmd.succeeded)
        ver = tuple(map(int, cmd.stdout.split('.')))
        self.assertGreaterEqual(ver, self.mod_vers['django'][0])
        self.assertLess(ver, self.mod_vers['django'][1])


    def test_module_versions(self):
        '''test all required modules for >=min and <max version'''
        import importlib as imp
        
        for name, verrange in self.mod_vers.items():
            min_v, max_v = verrange
            mod = imp.import_module(name)
            if hasattr(mod, '__version__'):
                ver = tuple(map(int, mod.__version__.split('.')))
            elif hasattr(mod, 'VERSION'):
                ver = mod.VERSION
            else:
                self.fail('No versoin string for %s' % name)
                
            self.assertGreaterEqual(ver, min_v)
            self.assertLess(ver, max_v)
            
            

#    def test_numpy_version(self):
#        import numpy as np
#        v = np.__version__.split('.')
#        self.assertGreaterEqual(v, self.numpy_req_ver)
#
#    def test_scipy_version(self):
#        import scipy as sp
#        v = sp.__version__.split('.')
#        self.assertGreaterEqual(v, self.scipy_req_ver)
#
#    def test_matplotlib_version(self):
#        import matplotlib as mpl
#        v = mpl.__version__.split('.')
#        self.assertGreaterEqual(v, self.mpl_req_ver)


# we use rabbitmq
#class ServerRedisTestCase(ut.TestCase):
#    
#    def setUp(self):
#        import redis
#        self.r = redis
#        try:
#            self.conn = redis.StrictRedis(host='localhost', port=6379, db=0)
#        except:
#            raise
#        
#    def test_01_connection(self):
#        try:
#            self.conn.info()
#        except self.r.ConnectionError:
#            self.fail("Connection to redis failed")
#        except:
#            raise
#            
#        
#    def test_02_save_and_retrieve(self):
#        val = 'blablabla'
#        self.conn.set('foo', val)
#        self.assertEqual(self.conn.get('foo'), val)
    
class ServerRabbitMQTestCase(ut.TestCase):
    
    def setUp(self):
        import pika
        self.pika = pika
        
    def test_01_connection(self):
        pass

    def test_02_basic_com_send(self):
        
        connection = self.pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.queue_declare(queue='hello')
        
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='Hello World!')
        print " [x] Sent 'Hello World!'"
        connection.close()

    def test_03_basic_com_recv(self):
        
        connection = self.pika.BlockingConnection()
        channel = connection.channel()
        method_frame, header_frame, body = channel.basic_get('test')
        if method_frame:
            print method_frame, header_frame, body
            channel.basic_ack(method_frame.delivery_tag)
        else:
            print 'No message returned'




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