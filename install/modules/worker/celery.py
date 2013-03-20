def about():
  return "production level worker distrubution server celery (using rabbitmq)"



def neededVars():
  vars = ()
  return vars



def beforePackageInstall():
  return (
    # add rabbitmq to sources
    ("echo deb http://www.rabbitmq.com/debian/ testing main >> /etc/apt/sources.list"),
    ("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc"),
    ("apt-key add rabbitmq-signing-key-public.asc"),
    ("rm rabbitmq-signing-key-public.asc"),
    ("apt-get update"),
  )


def getPackagesToInstall():
  return ('rabbitmq-server',)