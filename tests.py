#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shortcut to run local tests on the code


Created on Mon Nov 24 15:16:57 2014

@author: rafik
"""

import argparse
from deploy import tests

suites = [_[8:] for _ in tests.__dict__ if _.startswith('runSuite')]
    
    
    

parser = argparse.ArgumentParser()

parser.add_argument("command", help="which test to run", choices=suites)

args = parser.parse_args()

if args.command and args.command in suites:
    funcname = 'runSuite' + args.command
    try:
        tests.__dict__[funcname]()
    except:
        print 'bad luck running the test %s' % funcname
        
elif