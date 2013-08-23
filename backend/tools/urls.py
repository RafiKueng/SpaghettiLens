from django.conf.urls import patterns, url


from tools import views


urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^ResultDataTable$', views.ResultDataTable, name='ResultDataTable'),
    #url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
)