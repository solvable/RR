from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from .views import *


# Example url(r'^customers/$', "<appname>.views.<function_name>"),
urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'/customers'}, name='logout'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done , name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset , name='password_reset'),
    url(r'^password_reset/done/$',auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^user/$', get_user_profile, name="get_user_profile"),
    url(r'^$', index, name='index'),
    url(r'^search/', include('haystack.urls'), name='search'),
    url(r'^customer_browse/$', customer_browse, name='browse'),
    url(r'^recents/$', recents, name='recents'),
    url(r'^calendar/$', calendar, name='calendar'),
    url(r'^customer_create/$', customer_create, name='customer_create'),
    url(r'^open_workorders/$', open_workorders, name='open_workorders'),
    url(r'^(?P<id>\d+)/$', customer_detail, name='customer_detail'),
    url(r'^(?P<id>\d+)/edit/$', customer_update, name='customer_update'),
    url(r'^(?P<id>\d+)/delete/$', customer_delete, name='customer_delete'),
    url(r'^(?P<id>\d+)/jobsite_create/$', jobsite_create, name='jobsite_create'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/$', jobsite_detail, name='jobsite_detail'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/jobsite_update/$', jobsite_update, name='jobsite_update'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/jobsite_delete/$', jobsite_delete, name='jobsite_delete'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/appointment_create/$', appointment_create, name='appointment_create'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/appointment_detail/(?P<appId>\d+)/$', appointment_detail, name ='appointment_detail'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/appointment_detail/(?P<appId>\d+)/appointment_update/$', appointment_update, name ='appointment_update'),
    url(r'^(?P<id>\d+)/jobsite_detail/(?P<jobId>\d+)/appointment_detail/(?P<appId>\d+)/appointment_delete/$', appointment_delete, name ='appointment_delete'),
]


urlpatterns += staticfiles_urlpatterns()