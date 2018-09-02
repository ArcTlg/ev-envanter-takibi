# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import models
from . import views

app_name = 'app'

urlpatterns = [
    url(r'^$', views.BinaListView.as_view(), name='bina-list'),
    url(r'^bina/ekle/$', views.ModelCreateView.as_view(model=models.Bina), name='bina-ekle'),
    url(r'^bina/guncelle/(?P<pk>[0-9]+)/$',
        views.ModelUpdateView.as_view(model=models.Bina),
        name='bina-guncelle'),
    url(r'^bina/sil/(?P<pk>[0-9]+)/$',
        views.BinaDeleteView.as_view(model=models.Bina),
        name='bina-sil'),

    url(r'^(?P<bina_slug>[-\w]+)/$', views.DaireListView.as_view(), name='daire-list'),
    url(r'^(?P<bina_slug>[-\w]+)/daire/ekle/$',
        views.ModelCreateView.as_view(model=models.Daire),
        name='daire-ekle'),
    url(r'^daire/guncelle/(?P<pk>[0-9]+)/$',
        views.ModelUpdateView.as_view(model=models.Daire),
        name='daire-guncelle'),
    url(r'^daire/sil/(?P<pk>[0-9]+)/$',
        views.DaireDeleteView.as_view(model=models.Daire),
        name='daire-sil'),

    url(r'^(?P<bina_slug>[-\w]+)/(?P<daire_pk>[0-9]+)/$',
        views.OdaListView.as_view(),
        name='oda-list'),
    url(r'^(?P<bina_slug>[-\w]+)/(?P<daire_pk>[0-9]+)/oda/ekle/$',
        views.ModelCreateView.as_view(model=models.Oda),
        name='oda-ekle'),
    url(r'^oda/guncelle/(?P<pk>[0-9]+)/$',
        views.ModelUpdateView.as_view(model=models.Oda),
        name='oda-guncelle'),
    url(r'^oda/sil/(?P<pk>[0-9]+)/$',
        views.OdaDeleteView.as_view(model=models.Oda),
        name='oda-sil'),

    url(r'^(?P<bina_slug>[-\w]+)/(?P<daire_pk>[0-9]+)/(?P<oda_slug>[-\w]+)/$',
        views.EsyaListView.as_view(),
        name='esya-list'),
    url(r'^(?P<bina_slug>[-\w]+)/(?P<daire_pk>[0-9]+)/(?P<oda_slug>[-\w]+)/esya/ekle/$',
        views.ModelCreateView.as_view(model=models.Esya),
        name='esya-ekle'),
    url(r'^esya/guncelle/(?P<pk>[0-9]+)/$',
        views.ModelUpdateView.as_view(model=models.Esya),
        name='esya-guncelle'),
    url(r'^esya/sil/(?P<pk>[0-9]+)/$',
        views.EsyaDeleteView.as_view(model=models.Esya),
        name='esya-sil'),
]
