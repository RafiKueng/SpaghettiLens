from fabric.operations import sudo, prompt

me = "mysql"
type="database"

vars = {'host': 'localhost',
        'port': '1234',
        "user": ''}

def install():
  sudo('sudo apt-get install mysql')
  
  
def setup():
  pass
  
def getInfo():
  print "Getting data for database setup:"
  for var, val in vars.items():
    vars[var] = prompt(var, key=type+var, default=val)
    
  return vars

def getDjangoConfig():
  str = "blabla"
  return str