# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:11:04 2014

@author: rafik
"""





role_specific = {

    # for the role (and unique host) the dev server setup
    'dev' : {
        'foo'           : 'bar_dev',
        'code_dir'      : '/home/rafik/Projects/SpaghettiLens'
    },
    
    # for the role of a live server (there are 2 machines, the testing vm and the real live)
    'live' : {
        'foo'           : 'bar_live',    
        'code_dir'      : '/data/webapps/spaghettilens'
    },
    
    # specific setting for the testing server, overriding the live server ones
    'testing': {
        'foo'           : 'bar_live_test'
    },
    
    # for the role of a worker (there might be many, but only one setup needed usually)
    'worker' : {
        'foo'           : 'bar_worker',
        'code_dir'      : '/home/ara/rafik/src/SpaghettiLens'
    },
}