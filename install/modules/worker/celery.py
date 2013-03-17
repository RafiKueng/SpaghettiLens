import djcelery
djcelery.setup_loader()

INSTALLED_APPS += ('djcelery',)

BROKER_URL = ('amqp://'+
              BROKER_USER+':'+BROKER_PASSWORD+
              '@'+BROKER_HOST+':'+str(BROKER_PORT)+'/'+BROKER_VHOST)

CELERY_IMPORTS = ("lmt.tasks", )


WORKER_USED = "celery"