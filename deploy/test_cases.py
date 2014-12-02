# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:01:43 2014

@author: rafik
"""

import unittest as ut
#import os

#from settings import settings as _S







class test_server_setup(ut.TestCase):
    """Test if server setup is ready
    
    This runs locally on dev server and checks if remote server is available
    and basic stuff is set up.
    All other test will be run locally on the live server..
    """
    
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    def test_dirs_existing(self):
        pass







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