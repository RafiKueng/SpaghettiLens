from django.conf.urls import patterns, url

from lenses import views

urlpatterns = patterns('',

    url(r'^(?P<hash1>[0-9a-fA-F]{2})/(?P<hash2>[0-9a-fA-F]{62})/(?P<datatype>\w+)-(?P<datasource>\d{4})-(?P<subtype>\w+)\.(?P<ext>\w+)$',     views.getMedia, name='getMedia'),

    # for testing
    url(r'^(?P<hash1>[0-9a-fA-F]{2})/(?P<hash2>[0-9a-fA-F]{7})/(?P<datatype>\w+)-(?P<datasource>\d{4})-(?P<subtype>\w+)\.(?P<ext>\w+)$',     views.getMedia, name='getMedia'),

)
