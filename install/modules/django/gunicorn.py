from fabric.api import env


def about():
  return "production level django server gunicorn"


def getPackagesToInstall():
  return ('libevent-dev',)



def getPipPackagesToInstall():
  return ('greenlet',
          'gunicorn')


# override default here with os specific from the submodules  
if env.TARGET_OS == "deb":
  pass
else:
  raise BaseException("this module doesn't support the OS chosen")