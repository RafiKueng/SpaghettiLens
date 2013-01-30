from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lms.views.home', name='home'),
    # url(r'^lms/', include('lms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_modeldata/(?P<model_id>\d+)', 'Model.views.getModelData'),
    url(r'^save_model/', 'Model.views.saveModel'),
    url(r'^load_model/', 'Model.views.loadModel'),
    url(r'^calc_model/', 'Model.views.calcModel'),
   
)
