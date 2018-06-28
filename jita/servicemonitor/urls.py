
from django.conf.urls import url, include
from servicemonitor.views import home, register, uptimeregister, service, stop, start, equipment,add,stopped,started, breakdown, service_monitor, breakdownall
from django.contrib import admin

urlpatterns = [
        url(r'^stop/(?P<pk>[0-9]+)', stop, name='stop'),
        url(r'start/(?P<pk>[0-9]+)', start, name='start'),
        url(r'^$', home, name='home'),
        url(r'^register/$', register, name='register'),
        url(r'uptimeregister/', uptimeregister, name='uptimeregister'),
        url(r'service/', service, name='service'),
        url(r'equipment/', equipment, name='equipment'),
        url(r'add/', add, name='add'),
        url(r'stopped/(?P<pk>[0-9]+)',stopped, name='stopped'),
        url(r'started/(?P<pk>[0-9]+)', started, name='started'),
        url(r'^breakdown/$', breakdown, name='breakdown'),
        url(r'service_monitor/', service_monitor, name='service_monitor'),
        url(r'breakdownall', breakdownall, name='breakdownall'),
]