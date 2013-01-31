from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lmt.views.home', name='home'),
    # url(r'^lmt/', include('lmt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_modeldata/(?P<model_id>\d+)', 'ModellerApp.views.getModelData'),
    url(r'^save_model/', 'ModellerApp.views.saveModel'),
    url(r'^load_model/', 'ModellerApp.views.loadModel'),
    url(r'^result/(?P<result_id>\d+).json', 'ModellerApp.views.getSimulationJSON'),
    url(r'^result/(?P<result_id>\d+)/(?P<filename>.*\.\w{1,4}$)', 'ModellerApp.views.getSimulationFiles'),
    url(r'^data/', 'ModellerApp.views.getData'),
    
    
)
