from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


from .views import (
    index,
    customer_list,
    customer_create,
    customer_detail,
    customer_update,
    customer_delete,
    workorder_create,
    workorder_detail,
    workorder_delete,
    workorder_update,
    daily,

)


# Example url(r'^customers/$', "<appname>.views.<function_name>"),
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^search/', include('haystack.urls'), name='search'),
    url(r'^customer_list/$', customer_list, name='list'),
    url(r'^create/$', customer_create, name='create'),
    url(r'^(?P<id>\d+)/$', customer_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', customer_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', customer_delete),
    url(r'^(?P<id>\d+)/workorder_create/$', workorder_create, name='workorder_create'),
    url(r'^(?P<id>\d+)/workorder_detail/(?P<jobId>\d+)/$', workorder_detail, name='workorder_detail'),
    url(r'^(?P<id>\d+)/workorder_detail/(?P<jobId>\d+)/workorder_update/$', workorder_update, name='workorder_update'),
    url(r'^(?P<id>\d+)/workorder_detail/(?P<jobId>\d+)/workorder_delete/$', workorder_delete, name='workorder_delete'),
    url(r'^daily/$', daily, name='daily'),

]


urlpatterns += staticfiles_urlpatterns()