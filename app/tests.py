# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory

from django.contrib.auth.models import User

from app.models import Bina, Daire, Oda, Esya
from app import views


class LoginTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'secret123'}
        User.objects.create_user(**self.user_data)

    def test_register_user(self):
        response = self.client.get('/ev-envanter-takibi/kayit/')
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.client.get('/ev-envanter-takibi/giris/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/ev-envanter-takibi/giris/',
                                    self.user_data,
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_logout(self):
        response = self.client.get('/ev-envanter-takibi/cikis/')
        self.assertEqual(response.url, '/ev-envanter-takibi/giris/')


class ViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            'username': 'testuser',
            'password': 'secret123'}
        self.user = User.objects.create_user(**self.user_data)
        self.client.post('/ev-envanter-takibi/giris/',
                         self.user_data,
                         follow=True)

        self.bina = Bina(user=self.user, name='Apartman 1')
        self.bina.save()

        self.daire = Daire(bina=self.bina, no=1)
        self.daire.save()

        self.oda = Oda(daire=self.daire, name='Salon')
        self.oda.save()

        self.esya = Esya(oda=self.oda, name='Tv', price=1000)
        self.esya.save()

    def test_create_bina(self):
        bina_data = {'user': self.user, 'name': 'Test Apartmani'}
        request = self.factory.post('/bina/ekle/', bina_data)
        request.user = self.user

        response = views.ModelCreateView.as_view(model=Bina)(request)
        bina_sayisi = Bina.objects.all().count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(bina_sayisi, 2)

    def test_create_daire(self):
        daire_data = {'bina': self.bina, 'no': 2}
        url = '/%s/daire/ekle/' % self.bina.slug
        request = self.factory.post(url, daire_data)
        request.user = self.user

        response = views.ModelCreateView.as_view(model=Daire)(request, bina_slug=self.bina.slug)
        daire_sayisi = Daire.objects.all().count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(daire_sayisi, 2)

    def test_create_oda(self):
        oda_data = {'daire': self.daire, 'name': 'Salon'}
        url = '/%s/%s/daire/ekle/' % (self.bina.slug, self.daire.pk)
        request = self.factory.post(url, oda_data, follow=True)
        request.user = self.user

        response = views.ModelCreateView.as_view(model=Oda)(request,
                                                            bina_slug=self.bina.slug,
                                                            daire_pk=self.daire.pk)
        daire_sayisi = Oda.objects.all().count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(daire_sayisi, 2)

    def test_create_esya(self):
        esya_data = {'daire': self.daire, 'name': 'Tv', 'price': 1000}
        url = '/%s/%s/%s/esya/ekle/' % (self.bina.slug, self.daire.pk, self.oda.slug)
        request = self.factory.post(url, esya_data, follow=True)
        request.user = self.user

        response = views.ModelCreateView.as_view(model=Esya)(request,
                                                             bina_slug=self.bina.slug,
                                                             daire_pk=self.daire.pk,
                                                             oda_slug=self.oda.slug)
        esya_sayisi = Esya.objects.all().count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(esya_sayisi, 2)

    def test_update_bina(self):
        bina_data = {'name': 'Update Apartmani'}

        url = '/bina/guncelle/%s/' % self.bina.pk

        request = self.factory.post(url, bina_data, follow=True)
        request.user = self.user

        response = views.ModelUpdateView.as_view(model=Bina)(request, pk=self.bina.pk)

        bina = Bina.objects.get(pk=self.bina.pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(bina.name, bina_data['name'])

    def test_update_daire(self):
        daire_data = {'no': 2}
        print (self.daire)
        url = '/daire/guncelle/%s/' % self.daire.pk

        request = self.factory.post(url, daire_data, follow=True)
        request.user = self.user

        response = views.ModelUpdateView.as_view(model=Daire)(request,
                                                              pk=self.daire.pk,
                                                              bina_slug=self.bina.slug)

        self.assertEqual(response.status_code, 200)

    def test_update_oda(self):
        oda_data = {'name': 'Mutfak'}

        url = '/oda/guncelle/%s' % self.oda.pk

        request = self.factory.post(url, oda_data, follow=True)
        request.user = self.user

        response = views.ModelUpdateView.as_view(model=Oda)(request, pk=self.oda.pk)

        self.assertEqual(response.status_code, 200)

    def test_update_esya(self):
        esya_data = {'name': 'Buzdolabi', 'price': 750}

        url = '/esya/guncelle/%s' % self.esya.pk

        request = self.factory.post(url, esya_data, follow=True)
        request.user = self.user

        response = views.ModelUpdateView.as_view(model=Esya)(request, pk=self.esya.pk)

        self.assertEqual(response.status_code, 200)

    def test_delete_esya(self):
        url = '/esya/sil/%s/' % self.esya.pk
        request = self.factory.post(url)
        request.user = self.user

        response = views.EsyaDeleteView.as_view(model=Esya)(request, pk=self.esya.pk)
        esya_sayisi = Esya.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(esya_sayisi, 0)

    def test_delete_oda(self):
        url = '/oda/sil/%s/' % self.oda.pk
        request = self.factory.post(url)
        request.user = self.user

        response = views.OdaDeleteView.as_view(model=Oda)(request, pk=self.oda.pk)
        oda_sayisi = Oda.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(oda_sayisi, 0)

    def test_delete_daire(self):
        url = '/daire/sil/%s/' % self.daire.pk
        request = self.factory.post(url)
        request.user = self.user

        response = views.DaireDeleteView.as_view(model=Daire)(request, pk=self.daire.pk)
        daire_sayisi = Daire.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(daire_sayisi, 0)

    def test_delete_bina(self):
        url = '/bina/sil/%s/' % self.bina.pk
        request = self.factory.post(url)
        request.user = self.user

        response = views.BinaDeleteView.as_view(model=Bina)(request, pk=self.bina.pk)
        bina_sayisi = Bina.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(bina_sayisi, 0)

    def test_get_bina_list(self):
        url = '/'
        request = self.factory.get(url)
        request.user = self.user

        response = views.BinaListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_get_daire_list(self):
        url = '/%s/' % self.bina.slug
        request = self.factory.get(url)
        request.user = self.user

        response = views.DaireListView.as_view()(request, bina_slug=self.bina.slug)

        self.assertEqual(response.status_code, 200)

    def test_get_oda_list(self):
        url = '/%s/%s/' % (self.bina.slug, self.daire.pk)
        request = self.factory.get(url)
        request.user = self.user

        response = views.OdaListView.as_view()(request,
                                               bina_slug=self.bina.slug,
                                               daire_pk=self.daire.pk)

        self.assertEqual(response.status_code, 200)

    def test_get_esya_list(self):
        url = '/%s/%s/%s/' % (self.bina.slug, self.daire.pk, self.oda.slug)
        request = self.factory.get(url)
        request.user = self.user

        response = views.EsyaListView.as_view()(request,
                                                bina_slug=self.bina.slug,
                                                daire_pk=self.daire.pk,
                                                oda_slug=self.oda.slug)

        self.assertEqual(response.status_code, 200)
