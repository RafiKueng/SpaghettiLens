 # -*- coding: utf-8 -*-
"""
This tests the basic setup of the server

Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""


import unittest as ut


"""
This runs locally on dev server and checks if remote server is available
and basic stuff is set up.
All other test will be run locally on the live server..
"""
class test_server_setup(ut.TestCase):
    
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    def test_dirs_existing(self):
        pass
        
        
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()