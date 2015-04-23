from __future__ import division, with_statement, absolute_import
import sys, getopt, os, traceback

from glass.environment import env, Environment
from glass.command import command, Commands
from glass.exmass import * #PointMass
from glass.exceptions import GLInputError


@command('Load a glass basis set')
def glass_basis(env, name, **kwargs):
    #print __builtins__
    env.basis_options = kwargs
    f = __import__(name, globals(), locals())
    for name,[f,g,help_text] in Commands.glass_command_list.iteritems():
        if __builtins__.has_key(name):
            print 'WARNING: Glass command %s (%s) overrides previous function %s' % (name, f, __builtins__.__dict__[name])
        __builtins__[name] = g




#if len(sys.argv) < 2: help()

Environment.global_opts['ncpus_detected'] = 2
Environment.global_opts['ncpus'] = 2
Environment.global_opts['omp_opts'] = {} #_detect_omp()
Environment.global_opts['withgfx'] = True

Commands.set_env(Environment())

if Environment.global_opts['withgfx']:
    import glass.plots 

import glass.glcmds
import glass.scales
#import pytipsy 

#with open(arglist[0], 'r') as f:
    #Commands.get_env().input_file = f.read()

#Environment.global_opts['argv'] = arglist
##Commands.get_env().argv = arglist


#try:
    #execfile(arglist[0]) #, globals(), globals())
#except GLInputError as e:
    #tb = traceback.extract_tb(sys.exc_traceback, 2)[1]
    ##traceback.print_tb(sys.exc_traceback, 2)
    #print >>sys.stderr, "Input error on line %i of file '%s':" % (tb[1], tb[0])
    #print >>sys.stderr, "> %s" % tb[3]
    #print >>sys.stderr
    #print >>sys.stderr, e
    #print >>sys.stderr
