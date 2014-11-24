#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shortcut to run local tests on the code


Created on Mon Nov 24 15:16:57 2014

@author: rafik
"""

import argparse

#suites = [_[8:] for _ in tests.__dict__ if _.startswith('runSuite')]
#others = ['django']
#
#choices = suites + others
#
#parser = argparse.ArgumentParser()
#parser.add_argument("command", help="which test to run", choices=choices)
#args = parser.parse_args()
#
#
#if args.command and args.command in suites:
#    funcname = 'runSuite' + args.command
#    try:
#        tests.__dict__[funcname]()
#    except:
#        print 'bad luck running the test %s' % funcname
#
#        
#elif args.command in others:
#    
#    if args.command == 'django':
#        pass




def static_analysis():
    print("in static")
    pass

def django_unittest():
    pass

def django_functional():
    pass

def global_functional():
    pass







def main():

    choices = {
        'static': static_analysis, 
        'django_unit': django_unittest, 
        'django_func': django_functional,
        'global_func': global_functional,
    }
    
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="which test to run", choices=choices.keys())
    args = parser.parse_args()
    
    choices[args.command]()



if __name__ == "__main__":
    main()