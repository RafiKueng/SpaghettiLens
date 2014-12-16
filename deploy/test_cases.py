# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:01:43 2014

@author: rafik
"""
from __future__ import absolute_import


import sys
#import os

import unittest as ut

from fabric.api import run, env, cd, local, hide, warn_only
#from .fab_tools import GetOutOfLoop
#from .fab_tools import inform, warnn, lmanagepy, errorr, confirm, choose

from .settings import settings as _S




_E = env



    
def _local(cmd):
    #print 'hiding'
    with hide('running', 'output', 'warnings'), warn_only():
        return local(cmd, capture=True)



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
            'celery':       [(3,1,17), (3,2)],
            
        }
        
        self.py_req_version = (2,7)
        self.py_max_version = (3,0) # dont allow python3
        self.django_req_ver = (1,7)
        
        
    
    def test_01_python_version(self):
        '''test version of python'''
        self.assertGreaterEqual(sys.version_info, self.py_req_version)
        self.assertLess(sys.version_info, self.py_max_version)
        
        
    def test_managepy_version(self):
        '''test the local manage.py reported version'''
        
        cmd = _local("python %s/manage.py --version" % _S.APPS.DIR)
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
            
class ServerErlangTestCase(ut.TestCase):

    def setUp(self):
        self.ver_min = (16,1)
        self.ver_max = (99,99)
    

    def test_available(self):
        cmd = _local("erl -noshell -eval 'io:fwrite(\"~s\n\", [erlang:system_info(otp_release)]).' -s erlang halt")
        
        self.assertTrue(cmd.succeeded, "'erl command not available'")
        
        try:
            v = cmd.stdout[1:].split('B')
        except:
            v = cmd.stdout.split('.')
        v = tuple(map(int, v))
            
        self.assertGreaterEqual(v, self.ver_min, 'erlang version too old')
        self.assertLess(v, self.ver_max, 'erlang version too recent')

 
class ServerRabbitMQTestCase(ut.TestCase):
    
    def setUp(self):
        import puka

        self.Client = puka.Client
        
        #amqpurl = 'amqp://guest:guest1@192.168.100.10:5672/'
        self.amqpurl = 'amqp://guest:guest1@192.168.100.10:5672/'
        self.msg = "test msg\nmumumumultiline"
        self.queue = 'testing'
        self.exchange = ''
        
        #self.producer = puka.Client(amqpurl)
        #self.consumer = puka.Client(amqpurl)

    def test_00_service_available(self):
        stdout = _local('systemctl | grep rabbitmq')
        #print c
        self.assertIn('rabbitmq-server.service', stdout)
        self.assertIn('loaded', stdout)
        self.assertIn('active', stdout)
        self.assertIn('running', stdout)
        
        
    def test_01_connection(self):

        client = self.Client(self.amqpurl)
        try:
            # connect client
            promise = client.connect()
            client.wait(promise)
            client.wait(client.close())

        except:
#            raise
            self.fail("connection error")
            
        
    def test_02_create_queue(self):

        client = self.Client(self.amqpurl)

        client.wait(client.connect())

        # declare queue (queue must exist before it is being used - otherwise messages sent to that queue will be discarded)
        client.wait(client.queue_declare(queue=self.queue))
        client.wait(client.queue_purge(queue=self.queue))
        
        client.wait(client.close())
        


    def test_03_send_msg_to_queue(self):
        # send message to the queue named rabbit

        producer = self.Client(self.amqpurl)
        producer.wait(producer.connect())

        send_promise = producer.basic_publish(exchange=self.exchange, routing_key=self.queue, body=self.msg)
        producer.wait(send_promise)

        producer.wait(producer.close())


    def test_04_recv_msg_from_queue(self):
        # start waiting for messages, also those sent before (!), on the queue named rabbit

        consumer = self.Client(self.amqpurl)
        consumer.wait(consumer.connect())

        receive_promise = consumer.basic_consume(queue=self.queue, no_ack=True)
        received_message = consumer.wait(receive_promise, timeout=0.1)
        
        self.assertEqual(received_message['body'], self.msg)
        self.assertEqual(received_message['exchange'], self.exchange)
        self.assertEqual(received_message['routing_key'], self.queue)
        
        consumer.wait(consumer.close())

        
    def test_complex_send_and_receive(self):

        import random
        nmsg = 10
        rng = range(nmsg)
        rnd = random.randint(0,100)
        
        #self.queue = 'rab'

        producer = self.Client(self.amqpurl)
        consumer = self.Client(self.amqpurl)
        
        # connect
        producer.wait(producer.connect())
        consumer.wait(consumer.connect())
        
        # declare queue (queue must exist before it is being used - otherwise messages sent to that queue will be discarded)
        producer.wait(producer.queue_declare(queue=self.queue))
        producer.wait(producer.queue_purge(queue=self.queue))
        
        # send message to the queue named rabbit
        for i in rng:
            producer.wait(producer.basic_publish(exchange='', routing_key=self.queue, body='%i;%i'%(i,i*rnd)))
        producer.wait(producer.basic_publish(exchange='', routing_key=self.queue, body='/END'))
        
        # start waiting for messages, also those sent before (!), on the queue named rabbit
        receive_promise = consumer.basic_consume(queue=self.queue, no_ack=True)
        
        msgnr = 0
        
        while True:
            
            msg = consumer.wait(receive_promise, timeout=0.1)
            #print msg
            try:
                msg = msg['body']
            except:
                self.fail("Bad (empty) message received / timeout: " + str(msg))

            msgnr += 1
            
            if msg == '/END':
                self.assertEqual(msgnr, nmsg+1, "Not same amount of msg recv than sended") #+1 because of additional /END tag
                # check if /END is last msg in queue:
                msg = consumer.wait(receive_promise, timeout=0.1)
                self.assertIsNone(msg)
                break
            
            elif msgnr > nmsg + 1:
                self.fail("Too many messages received")

            elif msg is None: #this should actually never happen
                self.assertEqual(msgnr, nmsg+1, "Not same amount of msg recv than sended") #+1 because of additional /END tag
                break

            
            try:
                i, j = map(int, msg.split(';'))
                self.assertTrue(i * rnd == j)
            except:
                self.fail("strage msg received: %s" % msg)


        producer.wait(producer.close())
        consumer.wait(consumer.close())






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