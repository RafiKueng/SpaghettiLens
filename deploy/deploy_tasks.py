# -*- coding: utf-8 -*-
"""


Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""
from __future__ import absolute_import


from fabric.api import cd, prefix, local, put, puts, settings, run, abort, env, task, sudo, prompt  #*
#from fabric.utils import *

#from fabric import operations as ops
from fabric import colors
from fabric.contrib import console, files, project


from .fab_tools import check_or_create_dirs, inform, warnn, debugmsg, localc, rvenv

from .settings import settings as _S


#from pprint import pprint
from datetime import datetime as dt
import os
from attrdict import AttrDict
#import tempfile
#import shutil



DEBUG = True

# _S are the static settings (not to be updated)
# _E are the current settings
_E = env


@task()
def update_files():
    '''just uploads the files, usefull for testing the unittests on tmp server

    only works after one successful deploy_server    
    '''
    _E.INSTALL_DIR = '/tmp/swlabs' #'real' install dir
    _copy_files_server()
    
    
    
@task()
def test_srv():
    _generate_version_information()
    _E.INSTALL_DIR = '/tmp/swlabs' #'real' install dir
    _copy_files_server()
    _test_server_setup()




@task()
def deploy_server():
    '''Deploys the server
    
    tests if all required daemons are running, if not, installs them
    '''

    inform("install of server")
    
    _E.INSTALL_DIR = '/tmp/swlabs' #'real' install dir
    
    _check_if_local_branch_is_master()
    _generate_version_information()

    _copy_files_server()

    with cd(_E.INSTALL_DIR):

        _setup_py_pip_venv()
        _setup_django_config_files()


    _E.SERVERSETUPTEST_PASSED = _test_server_setup_in_adv()
    
    _install_missing_server_software(_E.SERVERSETUPTEST_PASSED)
    
    tests_passed = _test_server_setup()
    for test, result in tests_passed:
        puts('%-20s: %s' % (test, str(result)))
   
    

    


@task()
def deploy_worker():
    
    _check_if_local_branch_is_master()
    _generate_version_information()
    _setup_dirs_and_copy_files_worker()

        
    with cd(_E.INSTALL_DIR):

        _setup_py_pip_venv()
        _setup_django_config_files()            
        _build_and_setup_glass()        
        
        # set up the start scripts
            
        # run the tests

        # FOR DEBUG ONLY, make site pagackes available, so no need to compile numpy ect
        if DEBUG:
            #run('rm %s' % (os.path.join(_E.INSTALL_DIR, _S.PYENV_DIR, 'lib', 'python2.7','no-global-site-packages.txt')))
            pass # we already enabled site packages, because no need to build numpy..



    
    with cd(_S.ROOT_PATH):
        if files.exists('_current'):
            run('rm _current')
        run('ln -s %s _current' % _E.VERSION.version_str)

        
        if not DEBUG:
            run('rm -rf _current/{TMPDIR}'.format(**_S))
        else:
            debugmsg("Skipping cleanup")
        
        
        
    # create startup scripts
    
        



def _copy_files_server():

    newsubdirs = [
        _S.APPS.DIR,
        _S.APPS.MEDIA_DIR,
        _S.TMPDIR,
        'deploy',
    ]

    # dirs to copy (src, dest)
    dirstocopy = [
        (_S.SRC.DJANGODIR, _S.APPS.DIR),
        ('deploy', 'deploy'),
    ]

    # single files to copy (src, dest, destname)
    filestocopy = [
        (_S.SRC.PIP_REQ_RPATH_SRV, _S.TMPDIR, 'pip_requirements.txt')
    ]

    _setup_dirs_and_copy_files(filestocopy, dirstocopy, newsubdirs)





def _generate_django_config_file_str(settings_dic):

# FOR TESTING _generate...
#    sett = AttrDict({
#        'DATABASE' : {
#            'NAME'  : 'blabla',
#            'CONN'  : {'H':12, 'P':154}
#        },
#        'USER' : 'Bla'
#    })
    
    def d_eval(val, prefix=''):
        #print val, prefix

        if isinstance(val,dict) or isinstance(val, AttrDict):
            if len(prefix)>0:
                prefix += '_'
            s = []
            for k, v in val.items():
                s.extend(d_eval(v, prefix+k))
            return s
        else:
            if len(prefix) > 24:
                assert "error in creating config file.. string too long, adjust script"
            v = ("'%s'"%str(val)) if type(val)==str else str(val) # only put string in '..'
            #print prefix, v
            return ['%-24s = %s' % (prefix, v)]
    
    return '\n'.join(sorted(d_eval(settings_dic)))






def _setup_py_pip_venv():
    '''setup python, pip and virtualenv
    
    assumption:
    * we have  python, but nothing else (should work with python2 and 3, but will get venv with py2)
    * will be installed in the current dir
    solution: create a local python (~~/.local/bin)
    which is used to create a virtualenv
    Make sure the local pip is on path "~/.local/bin"
    
    http://forcecarrier.wordpress.com/2013/07/26/installing-pip-virutalenv-in-sudo-free-way/
    '''
    
    inform("Setup Python, Pip and the VirtualEnv")

    with settings(warn_only=True):
        cmd = run('python --version')        
        if cmd.failed or '2.7' not in cmd:
            abort('No python 2.7 available remote... aborting')
        cmd = run('pip -V')
        if cmd.failed or 'python 2.7' not in cmd:
            warnn('no pip found remote. getting and installing a remote version into ~/.local/bin')
            run('curl -O https://bootstrap.pypa.io/get-pip.py')
            run('python get-pip.py --user')
            warnn('Make sure the local pip is on path "~/.local/bin" (~/.bashrc)')
            if not console.confirm('Finished putting it on path?'):
                abort('then do it now!!')

    with settings(warn_only=True):
        if run('virtualenv --version').failed:
            warnn('no virtualenv found, installing a local (--user) one using pip')
            run('pip install --user virtualenv')
    
    run('virtualenv -p python --system-site-packages %s' %_S.PYENV_DIR) #using numpy from system..
    
    # instal python packages into virtualenv
    with prefix('source %s' % os.path.join(_S.PYENV_DIR, 'bin/activate')):
#        if not DEBUG:
        run('pip install -r {TMPDIR}/{SRC.PIP_REQ_FILE}'.format(**_S))
#        else:
#            debugmsg('skipping local installation of python modules') # because build of numpy take some time..

# make sure to have on opensuse: (sudo zypper)
# - python-numpy-devel
# - python-scipy-devel
# - python-matplotlib-devel



def _setup_django_config_files():
    ''' set up the config files
    Assumptions:
    * we are currently in the install dir..
    '''

    inform('Setup Django Configuration Files')

    sett = _S.django_celery_worker_config
    sett.update({'ROLE': 'production_worker'}) # or use env.django_role

    cstr = _generate_django_config_file_str(sett)

    run('mkdir -p {APPS.SETTINGS_RPATH}'.format(**_S))        #TODO remove this, it should be in the main tree by now
    run('touch {APPS.SETTINGS_MACHINE}'.format(**_S))
    files.append(_S.APPS.SETTINGS_MACHINE, cstr) #, escape=False)

    puts(colors.magenta("Getting Secrets from file or console..."))
    # set up the secrets in the config file
    required_secrets = [
        'DATABASE_USER',
        'DATABASE_PASSWORD',
        'BROKER_USER',
        'BROKER_PASSWORD'
    ]
    secrets = {}
    
    try:
        import secret_settings
    except ImportError:
        secret_settings = None
        warnn('No predefined secrets found in secret_settings.py!\nPlease enter the secrets manually:')
    for sec in required_secrets:
        try:
            val = secret_settings._[sec]
        except (KeyError, AttributeError):
            val = ''
        if not DEBUG:
            val = console.prompt('%s: ' % sec, default=val)
        else:
            debugmsg('skipping confirmation of secret settings (%s)'%sec)
        secrets[sec] = val
        
    cstr = _generate_django_config_file_str(secrets)
    files.append(_S.APPS.SETTINGS_SECRETS, cstr)


    # create versions file to keep track of version numbers
    cstr = '# version numbers\n\nversion = '
    cstr += repr(_E.VERSION)[1:].replace(',', ',\n   ').replace('{', '{\n    ').replace('}', '\n}') # convert to real python code with nice format
    files.append(_S.APPS.SETTINGS_VERSION, cstr)


  
def _generate_version_information():

    inform('Gathering version information')

    local('git fetch --tags')

    lmt_version = localc('git describe --abbrev=6 --tags --match "v[0-9]*"') #TODO delete this once switched to new naming schema
    gls_version = localc('git describe --abbrev=0 --tags --match "gls\.v[0-9]*"')
    
    t = lmt_version.split('-')
    if len(t)==3:
        version, ahead, hashstr = t
    else:
        version = t[0]
        ahead = "0"
        hashstr = ""
    major, minor, revis = version[1:].split('.')
    
    timestamp = dt.now().strftime("%Y%m%d%H%M")
    
    lmt_version = (int(major), int(minor), int(revis), int(ahead), hashstr, timestamp)
    gls_version = int(gls_version[5:])
    
    version_str = '%s__%s__%s.%s.%s_%s' % (timestamp, hashstr, major, minor, revis, ahead)

    _E.VERSION = AttrDict({
        'major': major,
        'minor': minor,
        'revis': revis,
        'ahead': ahead,
        'hash' : hashstr,
        'timestamp': timestamp,
        'gls_file' : gls_version,
        'glass': _S.GLASS.COMMIT,
        'version_str' : version_str,
    })




def _check_if_local_branch_is_master():
    
    inform('Check the local git repro')
    
    curr_branch = local("git symbolic-ref --short -q HEAD", capture=True)

    if curr_branch != 'master':
        warnn("""You're not on the master branch (but on `%s`), but you try to update the workers.
Thats probably not what you want to do...
Check commit your changes and merge with master, then test, then update the worker nodes."""%curr_branch)

        if not DEBUG:
            if not console.confirm("Continue anyways?", default=False):
                abort("Aborted due to wrong local branch")
        else:
            debugmsg("warning because working on non master branch '%s' cancleled" % curr_branch)
            
            
            
            
            
            
def _build_and_setup_glass():
    '''compile glass and its libraries with the make file in a temp dir and then rearrange things'''
    
    inform('Building and setting up glass')

    
    
    run('mkdir -p %s' % _S.GLASS.TMPBUILDDIR)
    
    run('git clone %s %s' % (_S.GLASS.REPROURL, _S.GLASS.TMPBUILDDIR))
    
    with cd(_S.GLASS.TMPBUILDDIR):

        run('git checkout %s' % _S.GLASS.COMMIT)

        with prefix('source %s' % os.path.join('..', _S.PYENV_DIR, 'bin/activate')):
            if not DEBUG:
                with settings(warn_only=True):
                    run('make -j4')
                    #if not files.exists('build/glpk_build/lib'):
                    #    run('mv build/glpk_build/lib64 build/glpk_build/lib') # bugfix
                    run('make')
            else:
                debugmsg('skipping building, because DEBUG is on..')
                run('cp -R ../../tmp_dev/build build')
            
    
    # which dirs / files to copy where..
    dirss  = (
        ('build/lib.linux-x86_64-2.7/',                 '%s/' % _S.EXTAPPS.DIR ),
        ('build/glpk_build/lib/',                       '%s/lib/' % _S.PYENV_DIR ),
        ('build/glpk_build/lib64/',                     '%s/lib/' % _S.PYENV_DIR ),
        ('build/python-glpk/lib.linux-x86_64-2.7/glpk', '%s/' % _S.EXTAPPS.DIR ),
    )

    for srcdir, destdir in dirss:
        run('mkdir -p %s' % destdir)
        with settings(warn_only=True): #prevent abort because lib or lib64
            run('rsync -pthrvz {src} {dest}'.format(**{
                'src'  : os.path.join(_S.GLASS.TMPBUILDDIR, srcdir),
                'dest' : os.path.join(_E.INSTALL_DIR, destdir),
            }))
        
    with cd(os.path.join(_E.INSTALL_DIR, _S.PYENV_DIR, 'lib')):
        run('ln -s libglpk.so.0.32.0 libglpk.so.0')
            
    
    # path the env for glass ext libs
    sstr  = 'LD_LIBRARY_PATH="$VIRTUAL_ENV/lib:$LD_LIBRARY_PATH"\nexport LD_LIBRARY_PATH\n\n'
    sstr += 'PYTHONPATH="$PYTHONPATH:{ROOT_PATH}/_current/{EXTAPPS.DIR}/glpk"\nexport PYTHONPATH\n'.format(**_S)
    files.append(os.path.join(_S.PYENV_DIR, 'bin','setenv'), sstr)
    files.append(os.path.join(_S.PYENV_DIR, 'bin','activate'), 'source setenv')

    #clean up
    if not DEBUG:
        run('rm -rf %s' % _S.GLASS.TMPBUILDDIR)
    else:
        debugmsg("Skipping cleanup")





def _setup_dirs_and_copy_files_worker():
    '''(insert functionname)

    assumes:
    * existing _E.VERSION version strings   
    
    #TODO: replace this with the more general version...
    '''
    
    inform('Setup the Dirs and copy the files for worker config')
    assert(_E.VERSION.version_str)


    _E.INSTALL_DIR = os.path.join(_S.ROOT_PATH, _E.VERSION.version_str) #'real' install dir

    check_or_create_dirs([
        _S.ROOT_PATH,
        _S.BIN_DIR,
        _E.INSTALL_DIR,
    ])

    # dirs to create    
    dirlist = [
        _S.APPS.DIR,
        _S.APPS.MEDIA_DIR,
        _S.TMPDIR,
    ]

    # dirs to copy (src, dest)
    dirsss = [
        (_S.SRC.DJANGODIR, _S.APPS.DIR)  
    ]

    # single files to copy (src, dest)
    filesss = [
        (_S.SRC.PIP_REQ_RPATH, os.path.join(_S.TMPDIR, _S.SRC.PIP_REQ_FILE))    
    ]


    with cd(_E.INSTALL_DIR):
        
        full_dirlist = [os.path.join(_E.INSTALL_DIR, d) for d in dirlist]
        check_or_create_dirs(full_dirlist)
        
        for srcdir, destdir in dirsss:
            project.rsync_project(
                remote_dir=os.path.join(_E.INSTALL_DIR, destdir),
                local_dir=os.path.join(srcdir, '') #appends trialing slash
            )
            
        for srcfile, destdir in filesss:
            put(local_path=srcfile, remote_path=os.path.join(_E.INSTALL_DIR, destdir))






def _setup_dirs_and_copy_files(filestocopy=[], dirstocopy=[], newsubdirs=[]):
    '''copies a list of files and dirs; and creates a few empty folders'''    
    
    inform('Setup the dirs and copy the files for the server')
    assert(_E.INSTALL_DIR)
    
    run('mkdir -p %s' % _E.INSTALL_DIR)
    
#    check_or_create_dirs([
#        _S.ROOT_PATH,
#        _S.BIN_DIR,
#        _E.INSTALL_DIR,
#        'deploy',
#    ])
#
#    # dirs to create    
#    dirlist = [
#        _S.APPS.DIR,
#        _S.APPS.MEDIA_DIR,
#        _S.TMPDIR,
#        'deploy',
#    ]
#
#    # dirs to copy (src, dest)
#    dirsss = [
#        (_S.SRC.DJANGODIR, _S.APPS.DIR),
#        ('deploy', 'deploy'),
#    ]
#
#    # single files to copy (src, dest)
#    filesss = [
#        (_S.SRC.PIP_REQ_RPATH_SRV, os.path.join(_S.TMPDIR, _S.SRC.PIP_REQ_FILE_SRV))    
#    ]


    with cd(_E.INSTALL_DIR):
        
        full_dirlist = [os.path.join(_E.INSTALL_DIR, d) for d in newsubdirs]
        check_or_create_dirs(full_dirlist)
        
        for srcdir, destdir in dirstocopy:
            fulldestdir = os.path.join(_E.INSTALL_DIR, destdir)
            run('mkdir -p %s' % fulldestdir)
            project.rsync_project(
                remote_dir=fulldestdir,
                local_dir=os.path.join(srcdir, '') #appends trialing slash
            )
            

        for srcfile, destdir, destfname in filestocopy:
            fulldestdir = os.path.join(_E.INSTALL_DIR, destdir)
            run('mkdir -p %s' % fulldestdir)
            if destfname is not None:
                fdestpath = os.path.join(fulldestdir, destfname)
            else:
                fdestpath = fulldestdir
            put(local_path=srcfile, remote_path=fdestpath)
            
            
#        run('touch %s'%os.path.join(_S.TMPDIR, _S.SRC.PIP_REQ_FILE))



def _test_server_setup_in_adv():
    '''tests the server setup prior to install from remote
    
    expects the repro to be uploaded to the working dir already
    
    returns if a certain testin case suite has succeded
    passed[0] = (redis, True)...
    passed is an ORDERED list
    '''
    inform('Testing the server setup')
    assert(_E.VERSION.version_str)
    

    #ordering is important
    tests = [
#        'redis': [
#            'ServerRedisTestCase',
##            'ServerRedisTestCase.test_01_connection',
#            ],
        ('pipdjango',    ['ServerDjangoTestCase',
                          ]),
        ('erlang',       ['ServerErlangTestCase.test_0_availability',
                          'ServerErlangTestCase.test_0_version',
                          ]),
        ('rabbitmq',     ['ServerRabbitMQTestCase.test_0_availability',
                          'ServerRabbitMQTestCase.test_0_version',
                          ]),
        ('couchdb',      ['ServerCouchDBTestCase.test_0_availability',
                          'ServerCouchDBTestCase.test_0_version',
                          ]),
        
    ]
    
    passed = []
    
    
    with cd(_E.INSTALL_DIR):
        
        if DEBUG:
            args = "-v"
        else:
            args = "-v --failfast"
        
        for sw, tests in tests:
            
            failed = False
            
            for test in tests:
                c = rvenv('python -m unittest %s deploy.test_cases.%s' % (args, test),
                        warn_only=True, quiet=False)
                lines = c.split('\n')
                if not 'OK' == c.split('\n')[-1]:
                    failed = True
                    break
                
            if not failed:
                passed.append((sw, True))
            else:
                passed.append((sw, False))
    
    return passed







def _test_server_setup():
    '''tests the server setup, are all services running and functioning?    
    
    expects the repro to be uploaded to the working dir already
    
    returns if a certain testin case suite has succeded
    passed[0] = (redis, True)...
    passed is an ORDERED list
    '''
    inform('Testing the server setup')
    assert(_E.VERSION.version_str)
    

    #ordering is important
    tests = [
#        'redis': [
#            'ServerRedisTestCase',
##            'ServerRedisTestCase.test_01_connection',
#            ],
        ('pipdjango',    ['ServerDjangoTestCase',
                          ]),
        ('erlang',       ['ServerErlangTestCase',]),
        ('rabbitmq',     ['ServerRabbitMQTestCase']),
        ('couchdb',      ['ServerCouchDBTestCase']),
        ('apache2',      ['ServerApache2TestCase']),
    ]
    
    passed = []
    
    
    with cd(_E.INSTALL_DIR):
        
        if DEBUG:
            args = "-v"
        else:
            args = "-v --failfast"
        
        for sw, tests in tests:
            
            failed = False
            
            for test in tests:
                c = rvenv('python -m unittest %s deploy.test_cases.%s' % (args, test),
                        warn_only=True, quiet=False)
                lines = c.split('\n')
                if not 'OK' == c.split('\n')[-1]:
                    failed = True
                    break
                
            if not failed:
                passed.append((sw, True))
            else:
                passed.append((sw, False))
    
    return passed





def _install_missing_server_software(tests_passed):
    '''if ceratin server software is not installed, then do it and set it up properly
    
    #TODO: for now only breaks the flow if failed    
    '''

    
#    apache
#    php
#    couchdb
#    rabbitmq
#    django
#    celery
#    flower

#    worker    

    for test, result in tests_passed:
        
        if not result:
            warnn("server hasn't installed: %s" % test)
            
            # PAY ATTENTION: ordering IS important (not here, but in the generation of the passed file..)
            
            if test == 'erlang':
                _server_erlang_install()
                # no config needed
                
            elif test == "rabbitmq":
                _server_rabbitmq_install()
                _server_rabbitmq_configure()
                
            elif test == "php":
                pass

            elif test == "apache":
                pass

            elif test == "couchdb":
                _server_couchdb_install()
                _server_couchdb_configure()

                
            else:
                if not DEBUG:           
                    abort("breaking because '%s' is missing" % test)






def _server_erlang_install():
    with cd(_S.TMPPATH):

        #old version..        
        #run('wget http://download.opensuse.org/repositories/openSUSE:/13.1/standard/x86_64/erlang-R16B01-2.1.3.x86_64.rpm')
        #sudo( 'zypper in erlang-R16B01-2.1.3.x86_64.rpm')
        
        sudo("zypper in unixODBC")

        # this works on opensuse 13.2
#        run("wget http://download.opensuse.org/repositories/openSUSE:/13.2/standard/x86_64/erlang-17.1-3.1.11.x86_64.rpm")
#        run("wget http://download.opensuse.org/repositories/openSUSE:/13.2/standard/x86_64/erlang-epmd-17.1-3.1.11.x86_64.rpm")
#        sudo("rpm -Uihv erlang-epmd-17.1-1.1.x86_64.rpm erlang-17.1-1.1.x86_64.rpm")
        
        #this works on opensuse 13.1?
#        run("wget http://download.opensuse.org/repositories/devel:/languages:/erlang:/Factory/openSUSE_13.1/x86_64/erlang-epmd-17.4-1.1.x86_64.rpm")
#        run("wget http://download.opensuse.org/repositories/devel:/languages:/erlang:/Factory/openSUSE_13.1/x86_64/erlang-17.4-1.1.x86_64.rpm")
#        sudo("rpm -Uihv erlang-epmd-17.4-1.1.x86_64.rpm erlang-17.4-1.1.x86_64.rpm")
        run("wget http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/erlang-epmd-17.4-3.1.x86_64.rpm")
        run("wget http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/erlang-17.4-3.1.x86_64.rpm")
        sudo("rpm -Uihv erlang-17.4-3.1.x86_64.rpm erlang-epmd-17.4-3.1.x86_64.rpm")


def _server_rabbitmq_install():
    with cd(_S.TMPPATH):
        run('wget http://download.opensuse.org/repositories/openSUSE:/13.1/standard/x86_64/rabbitmq-server-3.1.5-2.2.2.x86_64.rpm')
        sudo('rpm -Uihv rabbitmq-server-3.1.5-2.2.2.x86_64.rpm', warn_only=True)

        run("wget http://download.opensuse.org/repositories/openSUSE:/13.1/standard/x86_64/rabbitmq-server-plugins-3.1.5-2.2.2.x86_64.rpm")
        sudo("rpm -Uhiv rabbitmq-server-plugins-3.1.5-2.2.2.x86_64.rpm")



def _server_rabbitmq_configure():
    with cd(_S.TMPPATH):
        sudo("SuSEfirewall2 open EXT TCP {PORT}".format(**_S.RABBITMQ))
        sudo("SuSEfirewall2 stop")
        sudo("SuSEfirewall2 start")

        #run("chkconfig rabbitmq-server")
        #sudo("chkconfig rabbitmq-server on") #TODO needed?
        
        sudo("systemctl enable rabbitmq-server")
        sudo("systemctl start rabbitmq-server")
        sudo("rabbitmqctl status", warn_only=True)
        sudo("systemctl stop rabbitmq-server") #for some reason, an additional nrestart is needed
        sudo("rabbitmqctl status", warn_only=True)
        prompt('wait')
        sudo("systemctl start rabbitmq-server") #for some reason, an additional nrestart is needed
        sudo("rabbitmqctl status", warn_only=True)
        prompt('wait')
        
        sudo("rabbitmqctl add_user {USER} {PASSWORD}".format(**_S.RABBITMQ))
        sudo("rabbitmqctl add_vhost {VHOST}".format(**_S.RABBITMQ))
        sudo('rabbitmqctl set_permissions -p {VHOST} {USER} ".*" ".*" ".*"'.format(**_S.RABBITMQ))

        sudo('rabbitmqctl change_password guest {GUESTPSW}'.format(**_S.RABBITMQ))
        sudo('rabbitmqctl set_permissions -p {VHOST} guest ".*" ".*" ".*"'.format(**_S.RABBITMQ))

        #sudo("rabbitmq-plugins enable rabbitmq_management")


    sudo("systemctl restart rabbitmq-server")
    


def _server_couchdb_install():

    with cd(_S.TMPPATH):

        sudo("zypper in libmozjs185-1_0 libopenssl-devel")
    
    #sudo("wget http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/couchdb-1.6.1-47.1.x86_64.rpm")
    #sudo("rpm -Uihv couchdb-1.6.1-47.1.x86_64.rpm")

#    sudo("wget http://download.opensuse.org/repositories/server:/database/openSUSE_13.2/x86_64/couchdb-1.6.1-47.1.x86_64.rpm")
#    sudo("rpm -Uihv couchdb-1.6.1-47.1.x86_64.rpm")

        run("wget http://download.opensuse.org/repositories/server:/database/openSUSE_13.1/x86_64/couchdb-1.6.1-47.1.x86_64.rpm")
        sudo("rpm -Uihv couchdb-1.6.1-47.1.x86_64.rpm")
    
        sudo("chown -R couchdb:couchdb /etc/couchdb")
        sudo("chown -R couchdb:couchdb /var/lib/couchdb")
        sudo("chown -R couchdb:couchdb /var/log/couchdb")
        sudo("chown -R couchdb:couchdb /var/run/couchdb")
        
        sudo("chown -R couchdb:couchdb /etc/couchdb")
        sudo("chown -R couchdb:couchdb /var/lib/couchdb")
        sudo("chown -R couchdb:couchdb /var/log/couchdb")
        sudo("chown -R couchdb:couchdb /var/run/couchdb")
    
    
    
def _server_couchdb_configure():
    sudo("systemctl restart couchdb.service")