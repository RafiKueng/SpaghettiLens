from fabric.api import env

  

def about():
  return "production level mysql database server"


def neededVars():
  vars = (("DATABASE_HOST", "mqsql host", "localhost"),
          ("DATABASE_PORT", "port", "1234"),
          ("DATABASE_USER", "db username", "nothing"),
          ("DATABASE_NAME", "db name", "lmt"))
  return vars




def getPackagesToInstall():
  return ('mysql-server',)





