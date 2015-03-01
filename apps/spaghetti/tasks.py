# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 17:48:53 2015

@author: rafik
"""

from __future__ import division, with_statement, absolute_import
import sys, getopt, os, traceback, time

from paramiko import SSHClient
from scp import SCPClient
import paramiko

import matplotlib as mpl
from matplotlib import pyplot as plt
import pylab as pl

#from celery import shared_task
from _app.celery import app


#@app.task(bind=True)
#def runGLASS(self, jsonGLASSconfig):
#    
#    for i in range(40):
#        print i
#        time.sleep(0.5)
#        if not self.request.called_directly:
#            self.update_state(state='PROGRESS', meta={'solutions': ( i, 40)})
#    
#    return {}






@app.task(bind=True)
def runGLASS(self, GLASSconfig, config):
    
    print '='*80
    print "got GLASSconfig:\n"
    for k, v in GLASSconfig.items():
        print '%-16s : %s' % (k,v)
    print '='*80
    print "got config:\n"
    for k, v in config.items():
        print '%-16s : %s' % (k,v)
    print '='*80

    # don't take this outside, because only the worker has glass installed,
    # the webserver doesn't
    # so there will be import errors

    from glass.environment import env, Environment
    from glass.command import command, Commands
    from glass.exmass import PointMass
    from glass.exceptions import GLInputError


    @command('Load a glass basis set')
    def glass_basis(env, name, **kwargs):
        #print __builtins__
        env.basis_options = kwargs
        f = __import__(name, globals(), locals())
        for name,[f,g,help_text] in Commands.glass_command_list.iteritems():
            if __builtins__.has_key(name):
                print 'WARNING: Glass command %s (%s) overrides previous function %s' % (name, f, __builtins__[name])
            __builtins__[name] = g


    
    this = self
    
    def update_status(args):
        text = args['text']
        i, n = map(str, args['progress'])

        if not this.request.called_directly:
            this.update_state(state='PROGRESS', meta={'text':text, 'solutions': (i, n)})

        print ' '.join([text, i, 'of', n])

    #update_status({'text':'', 'progress':(0,0)})   
    update_status({'text':'init', 'progress':(0,0)})
    
    Environment.global_opts['ncpus_detected'] = 2
    Environment.global_opts['ncpus'] = 2
    Environment.global_opts['omp_opts'] = {} #_detect_omp()
    Environment.global_opts['withgfx'] = True
    
    Commands.set_env(Environment())
    
    if Environment.global_opts['withgfx']:
        import glass.plots 
    
    import glass.glcmds
    import glass.scales
    

    GC = GLASSconfig
    C = config
    
    logfile = "glass.log"


    glass_basis('glass.basis.pixels', solver='rwalk')
    meta(author=GC['author'], notes=GC['notes'])
    setup_log(logfile, stdout=True)
    samplex_random_seed(GC['random_seed'])
#    samplex_acceptance(rate=0.25, tol=0.15)
    samplex_acceptance(**GC['samplex_acceptance'])
    
    if GC['exclude_all_priors']:
        exclude_all_priors()

#    include_prior(
#        'lens_eq', 
#        'time_delay', 
#        'profile_steepness', 
#        'J3gradient', 
#        'magnification',
#        'hubble_constant',
#        'PLsmoothness3',
#        'shared_h',
#        'external_shear'
#    )
    include_prior(*GC['include_priors'])

#    hubble_time(13.7)
#    globject('B1115+080')

    hubble_time(GC['hubbletime'])
    globject(C['model_id']) 

    
#    zlens(0.31)  
#    pixrad(6)
#    steepness(0,None)
#    smooth(2,include_central_pixel=False)
#    local_gradient(45)
#    shear(0.01)
    zlens(GC['z_lens'])  
    pixrad(GC['pixrad'])
    steepness(*GC['steepness'])
    smooth(GC['smooth_val'],include_central_pixel=GC['smooth_ic'])
    local_gradient(GC['loc_grad'])
    shear(GC['shear'])
    if GC['isSym']:
        symm()
        
        
        
#    
#    A =  0.3550,  1.3220 
#    B = -0.9090, -0.7140
#    C = -1.0930, -0.2600
#    D =  0.7170, -0.6270
#    
#    source(1.722,   A,'min', 
#                    B,'min', 13.3,
#                    C,'sad', None,
#                    D,'sad', 11.7)

    print GC['source']
    source(*GC['source'])

    for i, exm in enumerate(GC['ext_masses']):
        external_mass(PointMass(exm['x'],exm['y'],name='PM%02i'%i), (0, exm['m']))

                    
    update_status({'text':'started modelling', 'progress':(0,0)})   

    model(GC['n_models'], update_hook=update_status)
    
    figpath = '/tmp/spaghettilens/'
    name = 'testing'
    path = os.path.join(figpath, name)

    try: # this prevents a race condition
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    update_status({'text':'create files', 'progress':(0,5)})   
    
    savestate(os.path.join(path, 'state.glass'))
    update_status({'text':'create files', 'progress':(1,5)})   

    env().make_ensemble_average()
    env().arrival_plot(env().ensemble_average, only_contours=True, colors='magenta', clevels=40)
    env().overlay_input_points(env().ensemble_average)
    pl.gca().axes.get_xaxis().set_visible(False)
    pl.gca().axes.get_yaxis().set_visible(False)
    pl.savefig(os.path.join(path, 'img1.png'))
    pl.close()
    update_status({'text':'create files', 'progress':(2,5)})   


    env().kappa_plot(env().ensemble_average, 0, with_contours=True, clevels=20, vmax=1, with_colorbar=False)
    pl.gca().axes.get_xaxis().set_visible(False)
    pl.gca().axes.get_yaxis().set_visible(False)
    pl.savefig(os.path.join(path, 'img2.png'))
    pl.close()
    update_status({'text':'create files', 'progress':(3,5)})   
    
    env().srcdiff_plot(env().ensemble_average)
    env().overlay_input_points(env().ensemble_average)
    pl.gca().axes.get_xaxis().set_visible(False)
    pl.gca().axes.get_yaxis().set_visible(False)
    pl.savefig(os.path.join(path, 'img3.png'))
    pl.close()
    update_status({'text':'create files', 'progress':(4,5)})   
    
    env().srcdiff_plot_adv(env().ensemble_average, night=True, upsample=8)
    env().overlay_input_points(env().ensemble_average)
    pl.savefig(os.path.join(path, 'img3_ipol.png'), facecolor='black', edgecolor='none')
    pl.close()
    update_status({'text':'create files', 'progress':(5,5)})


    # upload
    files = [
        'state.glass',
        'img1.png',
        'img2.png',
        'img3.png',
        'img3_ipol.png',
    ]
    host = config['upload_host']
    user = config['upload_user']
    destpath = config['upload_dest']

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user)
    scp = SCPClient(ssh.get_transport())
    
    update_status({'text':'upload files', 'progress':(0,5)})

    for i, f in enumerate(files):
        scp.put(os.path.join(path, f), os.path.join(destpath, f))
        update_status({'text':'upload files', 'progress':(i+1,5)})
        
  
    # ...
    #
    # model(1000, update_hook=update_status)
    # 
    
#    for i in range(40):
#        print i
#        time.sleep(0.5)
#        if not self.request.called_directly:
#            self.update_state(state='PROGRESS', meta={'solutions': ( i, 40)})
    
    return {}






######
# DEMO
##@shared_task
#@app.task(bind=True)
#def add(self, x, y):
#
#    print 0
#    
#    time.sleep(1)    
#    print 1
#
#    if not self.request.called_directly:
#        self.update_state(state='PROGRESS', meta={'current': 0, 'total': 2})
#
#
#    time.sleep(1)    
#    print 2
#
#    if not self.request.called_directly:
#        self.update_state(state='PROGRESS', meta={'current': 1, 'total': 2})
#
#    time.sleep(1)    
#    print 3
#
#    
#    if not self.request.called_directly:
#        self.update_state(state='PROGRESS', meta={'current': 2, 'total': 2})
#        
#    return x + y