from django.conf.urls import patterns, url

from lenses import views

urlpatterns = patterns('',
    url(r'^api$', views.api, name='api'),

    url(r'^get_gui$', views.getGui, name='getGui'),
)
