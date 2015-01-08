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

from fabric.api import env, abort
from deploy.fab_tools import warnn
from fabric.contrib.console import confirm
#from fabric import colors


tasks_that_need_role = {
    'deploy_worker',
    'deploy_server',
    'update_files',
    'test_srv',
    'dbg_run',
}



#TODO: more than one task should be possible now?!!
if len(env.tasks)>1:
    abort("More than one task specified (or none), Go slowly, young padawan..\nUse fab --list")


for t in env.tasks:
    #if len(env.tasks)==1 and env.tasks[0] in tasks_that_need_role:
    if t in tasks_that_need_role:
    
        if len(env.roles)>1: # or len(env.roles)==0:
            abort("More than one role specified, Go slowly, young padawan..")
        elif len(env.roles)==0:
            warnn("no role selected!")
            if confirm("Use default [dev]? (N to abort)", default=True):
                env.roles = ['dev']
            else:
                abort("User abort")



from deploy.deploy_tasks import *                                              # pylint: disable-msg=w0614
from deploy.test_tasks import *                                                # pylint: disable-msg=w0614

from deploy.settings import settings as _S

env.roledefs = _S.ROLEDEFS   # if error here: check settings file "if task in [...]" and tasks_that_need_role above


#@task()
#def _help():
#    warn('Specify what to do, and how as role..\nfab -R <role> <task>\n\nUse \'fab --list\' for more help / options')
