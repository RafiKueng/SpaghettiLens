from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import settings



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^spaghetti/', include('spaghetti.urls', namespace='spaghetti')),
    url(r'^lenses/',    include('lenses.urls',    namespace='lenses')),

#    url(r'^media/',     include('lenses.media_urls',    namespace='lenses')),
#    url(r'^getmedia/',  include('lenses.media_urls',    namespace='lenses')),

    url(r'^admin/', include(admin.site.urls)),
)


#
# generate the media / getmedia redirections
# (need both for debug server to work)
#
# DEBUG INFO:
# * MAKE SURE each installed app has a media_urls.py file
# * MAKE SURE the filter for custom apps on the next line stays correct!
#
installed_custom_apps = [_ for _ in settings.INSTALLED_APPS if 'django' not in _]

for app in installed_custom_apps:
    urlpatterns += patterns('',
        url('^media/%s/' % app,    include('%s.media_urls' % app, namespace=app)), 
        url('^getmedia/%s/' % app, include('%s.media_urls' % app, namespace=app))
    )
