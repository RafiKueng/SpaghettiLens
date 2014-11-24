from django.conf.urls import patterns, url

from spaghetti import views

urlpatterns = patterns('',
    url(r'^api$', views.api, name='api'),
)