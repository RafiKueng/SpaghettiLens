from django.conf.urls import patterns, url

from spaghetti import views

urlpatterns = patterns('',

    url(r'^(?P<hash1>[0-9a-fA-F]{2})/(?P<hash2>[0-9a-fA-F]{62})/(?P<filename>\w+)\.(?P<ext>\w+)$',
        views.getMedia, name='getMedia'),

    # for testing
    url(r'^(?P<hash1>[0-9a-fA-F]{2})/(?P<hash2>[0-9a-fA-F]{7})/(?P<filename>\w+)\.(?P<ext>\w+)$',
        views.getMedia, name='getMedia'),

#    # using shortcuts
#    url(r'^(?P<hash1>[0-9a-fA-F]{4})-(?P<hash2>[0-9a-fA-F]{4})/(?P<filename>\w+)\.(?P<ext>\w+)$',
#        views.getMedia, name='getMediaShort'),

        

)
