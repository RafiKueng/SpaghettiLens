from django.conf.urls import url

from LensesAPI import views

urlpatterns = [

    url(r'^api$',     views.api,    name='api'),
#    url(r'^get_gui$', views.getGui, name='getGui'),

]
