# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bina-ekle/$', views.bina_ekle, name='bina_ekle'),
    url(r'^(?P<bina_slug>[-\w]+)/$', views.bina, name='bina'),
    url(r'^(?P<bina_slug>[-\w]+)/daire-ekle/$', views.daire_ekle, name='daire_ekle'),
    url(r'^(?P<bina_slug>[-\w]+)/(?P<pk>[0-9]+)/$', views.daire, name='daire'),
    url(r'^(?P<bina_slug>[-\w]+)/(?P<pk>[0-9]+)/oda-ekle/$', views.oda_ekle, name='oda_ekle'),
    url(r'^(?P<bina_slug>[-\w]+)/(?P<pk>[0-9]+)/(?P<oda_slug>[-\w]+)/$',
        views.oda, name='oda'),
    url(r'^(?P<bina_slug>[-\w]+)/(?P<pk>[0-9]+)/(?P<oda_slug>[-\w]+)/esya-ekle/$',
        views.esya_ekle, name='esya_ekle'),
]
