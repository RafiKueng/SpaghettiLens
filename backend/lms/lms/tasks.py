from djcelery import celery



@celery.task
def calculateModel(x, y):
    return x + y