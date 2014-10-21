# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""

from fabric.api import *
from deploy.deploy import *

from deploy import settings
from deploy import tests



env.roledefs = {
    'dev': {
        'hosts': ['localhost'],
    },
    
    'testing': {
        'hosts': ['192.168.100.2'],
    },

    'production': {
        'hosts': ['swlabs.physik.uzh.ch'],
    },
    
    'worker': {
        'hosts': ['taurus.physik.uzh.ch'],
    },
    

}










def _set_env():
    if len(env.roles)>1: # or len(env.roles)==0:
        abort("More than one role specified or none, Go slowly, young padawan..")

    if 'dev' in env.roles:
        env.update(settings.role_specific['dev'])
    
    if 'production' in env.roles or 'testing' in env.roles:
        env.update(settings.role_specific['live'])

    if 'testing' in env.roles:
        env.update(settings.role_specific['testing'])

    if 'worker' in env.roles:
        env.update(settings.role_specific['worker'])




@task(default=True)
def deploy():
    _set_env()
    
    if 'worker' in env.roles:
        #abort('use deploy_worker')
        deploy_worker()
    elif 'production' in env.roles or 'testing' in env.roles:
        deploy_server()
    elif 'dev' in env.roles:
        deploy_dev()
    else:
        abort('specify a role using fab -R [role] deploy')


@task()
def test():
    _set_env()
    
    if 'worker' in env.roles:
        #abort('use deploy_worker')
        test_worker()
    elif 'production' in env.roles or 'testing' in env.roles:
        test_server()
    elif 'dev' in env.roles:
        test_dev()
    else:
        abort('specify a role using fab -R [role] test')
