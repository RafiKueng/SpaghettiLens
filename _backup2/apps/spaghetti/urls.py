from django.conf.urls import patterns, url

from spaghetti import views

urlpatterns = patterns('',
    url(r'^api$', views.api, name='api'),

    url(r'^model/(?P<model_id>[\w]{9,11})', views.getModel, name='getModel'),

    url(r'^', views.getIndex, name='getIndex'),


#    url(r'^celery_test$', views.celery_test, name='celery_test'),
#    url(r'^couch_test$', views.couch_test, name='couch_test'),
)
