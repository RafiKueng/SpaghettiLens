# -*- coding: utf-8 -*-
"""


Created on Thu Oct 16 15:51:20 2014

@author: rafik
"""


from fabric.api import *
from fabric.utils import *
from fabric import operations as ops

from fabric import colors

from fabric.contrib import console, files, project

#from fabric.contrib.console import confirm
#from fabric.contrib.files import *
#from fabric.contrib.project import *
#from fabric.colors import *

from fab_tools import *

from settings import settings as _S


from pprint import pprint
from datetime import datetime as dt
import os
from attrdict import AttrDict
import tempfile
import shutil



DEBUG = True




@task()
def deploy_server():
    print "instll"
    _check_or_create_dirs([_S.env.code_dir,])
    _install_pip()
    pass





@task()
def deploy_worker():
    
    curr_branch = local("git symbolic-ref --short -q HEAD", capture=True)

    if curr_branch != 'master':
        warn(colors.yellow("""You're not on the master branch (but on `%s`), but you try to update the workers.
Thats probably not what you want to do...
Check commit your changes and merge with master, then test, then update the worker nodes."""%curr_branch))
        if not console.confirm("Continue anyways?", default=False):
            abort("Aborted due to wrong local branch")
        
        
    
    inst_dir = _S.ROOT_PATH  #'/home/ara/rafik/tmp/apps/spaghettilens'
    bin_dir  = _S.BIN_DIR   #'/home/ara/rafik/tmp/local/bin'
    
    pyenv_dir = _S.PYENV_DIR # 'py_env'
    
    _check_or_create_dirs([inst_dir, bin_dir])

#    with cd(src_dir):
#        if exists(src_dir + '/.git'):
#            run('git pull origin master')
#        else:
#            run('git clone --branch master --depth 1 https://github.com/RafiKueng/SpaghettiLens.git .')

    local('git fetch --tags')
    #lmt_version = run('git describe --abbrev=6 --tags --match "lmt\.v[0-9]*"')
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

    version = {
        'major': major,
        'minor': minor,
        'revis': revis,
        'ahead': ahead,
        'hash' : hashstr,
        'timestamp': timestamp,
        'gls_file' : gls_version,
        'glass': '',
        'version_str' : version_str,
    }

    
    #pprint(lmt_version)
    #pprint(gls_version)
        
    rinst_dir = os.path.join(inst_dir, version_str) #'real' install dir
    _check_or_create_dirs([rinst_dir])

#    dirlist = [
#        'apps',
#        'tmp_media',
#        'deploy',
#    ]
#    
#    paths_to_copy = [
#        'apps',
#    ]
#
#    files_to_copy = [
#        _S.PIP_REQ_FILE,
#    ]

    
    dirlist = [
        _S.APPS.DIR,
        _S.APPS.MEDIA_DIR,
        _S.TMPDIR,
    ]
    dirsss = [
        (_S.SRC.DJANGODIR, _S.APPS.DIR)  
    ]

    
    filesss = [
        (_S.SRC.PIP_REQ_RPATH, os.path.join(_S.TMPDIR, _S.SRC.PIP_REQ_FILE))    
    ]



    with cd(rinst_dir):
        
        full_dirlist = [os.path.join(rinst_dir, d) for d in dirlist]
        _check_or_create_dirs(full_dirlist)
        
#        for loc in paths_to_copy:
#            put(local_path=loc, remote_path=rinst_dir)
#        for fil in files_to_copy:
#            put(local_path=fil, remote_path=os.path.join(rinst_dir, fil))
        for srcdir, destdir in dirsss:
            #put(local_path=srcdir, remote_path=os.path.join(rinst_dir, destdir))
            project.rsync_project(
                remote_dir=os.path.join(rinst_dir, destdir),
                local_dir=os.path.join(srcdir, '') #appends trialing slash
                )
            print srcdir, rinst_dir, destdir
            
        for srcfile, destdir in filesss:
            put(local_path=srcfile, remote_path=os.path.join(rinst_dir, destdir))
        
        # setup python, pip and virtualenv
        # assumption: we have  python, but nothing else
        # solution: create a local python (~~/.local/bin)
        # which is used to create a virtualenv
        
        #http://forcecarrier.wordpress.com/2013/07/26/installing-pip-virutalenv-in-sudo-free-way/

        with settings(warn_only=True):
            if run('python --version').failed:
                abort('No python available remote... aborting')
            if run('pip -V').failed:
                warn('no pip found remote. getting and installing a remote version into ~/.local/bin')
                run('curl -O https://bootstrap.pypa.io/get-pip.py')
                run('python get-pip.py --user')
                warn(colors.yellow('Make sure the local pip is on path "~/.local/bin" (~/.bashrc)'))
                if not console.confirm('Finished putting it on path?'):
                    abort('then do it now!!')

        run('pip install --user virtualenv')
        
        run('virtualenv %s' %pyenv_dir)
        
        with prefix('source %s' % os.path.join(pyenv_dir, 'bin/activate')):
            
            # instal python packages into virtualenv
            run('pip install -r {TMPDIR}/{SRC.PIP_REQ_FILE}'.format(**_S))
            
        # set up the config files
        sett = _S.django_celery_worker_config
        sett.update({'ROLE': 'production_worker'}) # or use env.django_role

        #pprint(sett)
        
        cstr = _generate_django_config_file_str(sett)

        pprint(cstr)
        
        run('mkdir -p {APPS.SETTINGS_RPATH}'.format(**_S))        #TODO remove this, it should be in the main tree by now
        run('touch {APPS.SETTINGS_MACHINE}'.format(**_S))
        files.append(_S.APPS.SETTINGS_MACHINE, cstr, escape=False)

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
            warn(colors.yellow('No predefined secrets found in secret_settings.py!\nPlease enter the secrets manually:'))
        for sec in required_secrets:
            try:
                val = secret_settings._[sec]
            except (KeyError, AttributeError):
                val = ''
            val = console.prompt('%s: ' % sec, default=val)
            secrets[sec] = val
            
        cstr = _generate_django_config_file_str(secrets)
        files.append(_S.APPS.SETTINGS_SECRETS, cstr, escape=False)
            
        
        # get and setup glass

        
        #we compile glass and its libraries with the make file in a temp dir and then rearrange things
        
#            tmpglass = os.path.join(_S.TMPPATH, 'glasstmp')
        tmpglass = _S.GLASS.TMPBUILDDIR
        
        run('mkdir -p %s' % tmpglass)
        
#            with cd(_S.TMPPATH):
        run('git clone %s %s' % (_S.GLASS.REPROURL, tmpglass))
        
        with cd(tmpglass):
            run('git checkout %s' % _S.GLASS.COMMIT)

        with cd(tmpglass):
            with prefix('source %s' % os.path.join('..', pyenv_dir, 'bin/activate')):
                with settings(warn_only=True):
                    run('make -j4')
                    run('make')
                
        
        # which dirs / files to copy where..
        dirss  = (
            ('build/lib.linux-x86_64-2.7/',                 '%s/' % _S.EXTAPPS.DIR ),
            ('build/glpk_build/lib/',                       '%s/lib/' % _S.PYENV_DIR ),
            ('build/python-glpk/lib.linux-x86_64-2.7/glpk', '%s/' % _S.EXTAPPS.DIR ),
#            ('/tmp/glass/build/lib.linux-x86_64-2.7/glass/', '/tmp/app/swlabs_worker/_current/ext_apps/glass/'),
#            ('/tmp/glass/build/glpk_build/lib/', '/tmp/app/swlabs_worker/_current/py_env/lib/'),
#            ('/tmp/glass/build/python-glpk/lib.linux-x86_64-2.7/glpk/','/tmp/app/swlabs_worker/_current/ext_apps/')
        )

        for srcdir, destdir in dirss:
            run('mkdir -p %s' % destdir)
            run('rsync -pthrvz {src} {dest}'.format(**{
                'src'  : os.path.join(tmpglass, srcdir),
                'dest' : os.path.join(rinst_dir, destdir),
            }))
            
        with cd(os.path.join(rinst_dir, _S.PYENV_DIR, 'lib')):
            run('ln -s libglpk.so.0.32.0 libglpk.so.0')
                
        
        # path the env for glass ext libs
        sstr  = 'LD_LIBRARY_PATH="$VIRTUAL_ENV/lib:$LD_LIBRARY_PATH"\nexport LD_LIBRARY_PATH\n\n'
        sstr += 'PYTHONPATH="$PYTHONPATH:{ROOT_PATH}/_current/{EXTAPPS.DIR}/glpk"\nexport PYTHONPATH\n'.format(**_S)
        files.append(os.path.join(_S.PYENV_DIR, 'bin','setenv'), sstr)
        files.append(os.path.join(_S.PYENV_DIR, 'bin','activate'), 'source setenv')
        
        

        #shutil.rmtree(tmpdir)
        version['glass'] = _S.GLASS.COMMIT
        
        
        # create versions file to keeep track of version numbers
        cstr = '# version numbers\n\nversion = '
#        for k, v in version.items():
#            cstr += '%s = \'%s\'\n' % (str(k), str(v))
        cstr += repr(version).replace(',', ',\n   ').replace('{', '{\n    ').replace('}', '\n}')
        files.append(_S.APPS.SETTINGS_VERSION, cstr, escape=False)


            
        # set up the start scripts
            
            
        # run the tests



        # FOR DEBUG ONLY, make site pagackes available, so no need to compile numpy ect
        if DEBUG:
            run('rm %s' % (os.path.join(rinst_dir, _S.PYENV_DIR, 'lib', 'python2.7','no-global-site-packages.txt')))



    
    with cd(inst_dir):
        if files.exists('_current'):
            run('rm _current')
        run('ln -s %s _current' % version_str)
    
    
    
    
    # setup virtualenv
#    with cd(src_dir):
#
#        pydir = os.path.join(src_dir, pyenv_dir)
#            
#        if not exists(os.path.join(pydir, 'bin/activate'), is_file=True):
#            run('virtualenv $s' % pyenv_dir)
#            
#            with prefix('source %s' % (os.path.join(pyenv_dir, 'bin/activate'))):
#                run('pip install -r deploy/requirements.txt')
                

    # create startup scripts
    
        








def _check_or_create_dirs(dirs=None):
    
    for d in dirs:
        run("mkdir -p %s" % d)
    
    
    #pprint(env)
    
    #puts("cocd with %s"%env.foo)

#    with settings(warn_only=True):
#        for d in dirs:
#            if run("test -d %s" % d).failed:
#                if .failed:
#                    print "using sudo to create dir!"                
#                    sudo("mkdir -p %s" % d)
#                    sudo("chmod 777 -r %s" % s) #TODO test this line
#                    #sudo("chown %s %s" % (user, d)) #TODO test this line


def _install_pip():
    with cd(code_dir):
        pass
    
    
def _init_or_update_git():

    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        #run("touch app.wsgi")
        
        
        
        
def _generate_django_config_file_str(settings_dic):
    
    sett = {
        'DATABASE' : {
            'NAME'  : 'blabla',
            'CONN'  : {'H':12, 'P':154}
        },
        'USER' : 'Bla'
    }
    

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
                assert "error in creating config file.. string too lnag, adjust script"
            return ['%-24s = "%s"' % (prefix, str(val))]
    
    return '\n'.join(sorted(d_eval(settings_dic)))















        
        
