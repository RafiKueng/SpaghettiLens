from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^spaghetti/', include('spaghetti.urls', namespace='spaghetti')),

    url(r'^admin/', include(admin.site.urls)),
)
