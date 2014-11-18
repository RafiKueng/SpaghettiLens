# -*- coding: utf-8 -*-
"""
Use the role to define whether the selected task/command should run on the testing infrastructure or on live.

General idea of deploy:
* You have the git repro locally.
* Check out the version / branch you want to deploy
  (should be master usually)
* Use fabric to deploy anything
 - select a task (those setup the different components of the system)
 - select a role (where / which machine to set up the task to, used for selection either the testing, stating and production machines)


Created on Thu Oct 16 15:51:20 2014
@author: rafik



Available Roles (-R) (usually, depends on task!):

    dev         run on the local machine
    test        run on the testing virtual machines
    prod        do it on the production server
"""

from deploy.deploy import *

#from deploy.settings import _ as _S
from deploy.settings import settings as _S
#from deploy import commands as _C
#from deploy import tests


#from pprint import pprint


env.roledefs = _S.ROLEDEFS


#pprint(env)



@task()
def help():
    warn('Specify what to do, and how as role..\nfab -R <role> <task>\n\nUse \'fab --list\' for more help / options')
