#supports only linux, ubuntu and debian

import fabric.api
from fabric.colors import *

from install.utils import _r, _s, _p
from install import *
from pickle import FALSE

from fabric.api import env
conf = env.conf

#################################################################################  

def about():
  return "production level mysql database server"


def neededVars():
  return (("DATABASE_HOST", "mysql host", "localhost"),
          ("DATABASE_PORT", "port", "3306"),
          ("DATABASE_ROOT_PSW", "mysql root password (existing or new one)", "demosqlroot"),#psw_gen()),
          ("DATABASE_NAME", "db name", "lmt"),
          ("DATABASE_USER", "db user name", "lmt"),
          ("DATABASE_PSW", "db user password", "lmt-sql-pw")#psw_gen())
         )


#################################################################################  


def installPackages():
  if conf['DATABASE_HOST']=='localhost':
    mysql_install()
  else:
    fabric.api.warn(yellow('make sure mysql is running on databse server'))


def installPipPackages():
  #pip_install('MySQL-python')
  pass


def postInstallCmds():
  mysql_create_user('root',
                    conf['DATABASE_ROOT_PSW'],
                    conf['DATABASE_USER'],
                    conf['DATABASE_PSW'])
  
  mysql_create_db(conf['DATABASE_USER'],
                  conf['DATABASE_PSW'],
                  conf['DATABASE_NAME'])


#################################################################################  






def _mysql_is_installed():
  with fabric.api.settings(fabric.api.hide('stderr'), warn_only=True):
    output = _r('mysql --version')
  try:
    return output.succeeded
  except AttributeError:
    return False



def mysql_install():
  """ Installs MySQL """
  if _mysql_is_installed():
    fabric.api.warn(yellow('MySQL is already installed.'))
    return
 
  # Ensure mysql won't ask for a password on installation
  # See the following:
  # http://serverfault.com/questions/19367/scripted-install-of-mysql-on-ubuntu
  # http://www.muhuk.com/2010/05/how-to-install-mysql-with-fabric/
 
  package_install('debconf-utils')
  
  # get the password
  passwd = fabric.api.env.conf['DATABASE_ROOT_PSW']
  
  # get the correct version for installation
  version = '5.5'
 
  debconf_defaults = [
    "mysql-server-%s mysql-server/root_password password %s" % (version,passwd),
    "mysql-server-%s mysql-server/root_password_again password %s" % (version,passwd),
  ]
 
  _s("echo '%s' | debconf-set-selections" % "\n".join(debconf_defaults))
 
  fabric.api.warn(yellow('The password for mysql "root" user will be set to "%s"' % passwd))
 
  common_packages = [
    'mysql-server-%s' % version,
  ]

  package_install(common_packages)
  
  
  
  
  
def mysql_start():
  """ Start MySQL """
  service('mysql','start')
 
def mysql_stop():
  """ Stop MySQL """
  service('mysql','stop')
 
def mysql_restart():
  """ Restart MySQL """
  service('mysql','restart')
 
 
def mysql_execute(sql, user='', password=''):
  """
  Executes passed sql command using mysql shell.
  """
  with fabric.api.settings(warn_only=True):
    return _r("echo '%s' | mysql -u%s -p%s" % (sql, user, password))
 
def mysql_create_db(user='',password='',database=''):
  """
  Creates an empty mysql database.
  """
  if not _mysql_is_installed():
    fabric.api.warn(yellow('MySQL must be installed.'))
    return
 
  if not user:
    user = fabric.api.prompt('Please enter username:')
  if not database:
    database = fabric.api.prompt('Please enter database name:')

  params = 'DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci'
  mysql_execute('CREATE DATABASE %s %s;' % (database, params), user, password)


def mysql_create_user(user='',password='',new_user='',new_password=''):
  """ Create a new mysql user. """
  if not _mysql_is_installed():
    fabric.api.warn(fabric.colors.yellow('MySQL must be installed.'))
    return
 
  if not user:
    user = fabric.api.prompt('Please enter username:')
  if not new_user:
    new_user = fabric.api.prompt('Please enter new username:')
  if not new_password:
    new_password = fabric.api.prompt('Please enter new password for %s:' % new_user)
 
    mysql_execute("""GRANT ALL privileges ON *.* TO "%s" IDENTIFIED BY "%s";FLUSH PRIVILEGES;""" % (new_user, new_password), user, password)
  
  