# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:43:52 2014

@author: rafik
"""

from fabric.api import *

def localc(s):
    return local(s, capture=True)


#def exists(path, is_dir=False, is_file=False):
#    with settings(warn_only=True):
#        if is_dir:
#            return run("test -d %s" % path).succeeded
#        elif is_file:
#            return run("test -f %s" % path).succeeded
#        else:
#            return run("test -e %s" % path).succeeded