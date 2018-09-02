# -*- coding: utf-8 -*-

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Bina, Daire, Oda, Esya


class BinaListView(ListView):
    model = Bina
    context_object_name = 'binalar'


class DaireListView(ListView):
    model = Daire
    context_object_name = 'daireler'

    def get_queryset(self):
        bina = Bina.objects.get(slug='%s' % (self.kwargs['bina_slug']))

        return Daire.objects.filter(bina=bina)

    def get_context_data(self, **kwargs):
        bina = Bina.objects.get(slug='%s' % (self.kwargs['bina_slug']))
        context = super(DaireListView, self).get_context_data(**kwargs)
        context['bina'] = bina

        return context


class OdaListView(ListView):
    model = Oda
    context_object_name = 'odalar'

    def get_queryset(self):
        daire = Daire.objects.get(pk=int(self.kwargs['daire_pk']))

        return Oda.objects.filter(daire=daire)

    def get_context_data(self, **kwargs):
        daire = Daire.objects.get(pk=int(self.kwargs['daire_pk']))
        context = super(OdaListView, self).get_context_data(**kwargs)
        context['daire'] = daire

        return context


class EsyaListView(ListView):
    model = Esya
    context_object_name = 'esyalar'

    def get_queryset(self):
        daire = Daire.objects.get(pk=int(self.kwargs['daire_pk']))
        oda = Oda.objects.get(slug='%s' % (self.kwargs['oda_slug']), daire=daire)

        return Esya.objects.filter(oda=oda)

    def get_context_data(self, **kwargs):
        daire = Daire.objects.get(pk=int(self.kwargs['daire_pk']))
        oda = Oda.objects.get(slug='%s' % (self.kwargs['oda_slug']), daire=daire)
        context = super(EsyaListView, self).get_context_data(**kwargs)
        context['oda'] = oda
        context['daire'] = daire

        return context


class ModelCreateView(CreateView):
    template_name = 'app/model_create_update_form.html'
    context_object_name = 'object'

    def __init__(self, *args, **kwargs):
        super(ModelCreateView, self).__init__(*args, **kwargs)
        if self.model.__name__ in ['Bina', 'Oda', 'Esya']:
            self.fields = ['name']
            if self.model.__name__ == 'Esya':
                self.fields.append('price')
        else:
            self.fields = ['no']

    def get_context_data(self, **kwargs):
        back_url = self.request.META['HTTP_REFERER']
        context = super(ModelCreateView, self).get_context_data(**kwargs)
        context['back_url'] = back_url

        return context

    def form_valid(self, form):
        model_name = self.model.__name__
        if model_name == 'Daire':
            bina = Bina.objects.get(slug=self.kwargs['bina_slug'])
            form.instance.bina = bina
        elif model_name == 'Oda':
            daire = Daire.objects.get(pk=self.kwargs['daire_pk'])
            form.instance.daire = daire
        elif model_name == 'Esya':
            daire = Daire.objects.get(pk=self.kwargs['daire_pk'])
            oda = Oda.objects.get(daire=daire, slug=self.kwargs['oda_slug'])
            form.instance.oda = oda

        return super(ModelCreateView, self).form_valid(form)


class ModelUpdateView(UpdateView):
    template_name = 'app/model_create_update_form.html'
    context_object_name = 'object'

    def __init__(self, *args, **kwargs):
        super(ModelUpdateView, self).__init__(*args, **kwargs)
        model_name = self.model.__name__
        if model_name == 'Bina':
            self.fields = ['name']
        elif model_name == 'Esya':
            self.fields = ['oda', 'name', 'price']
        elif model_name == 'Oda':
            self.fields = ['daire', 'name']
        else:
            self.fields = ['bina', 'no']

    def get_context_data(self, **kwargs):
        back_url = self.request.META['HTTP_REFERER']
        context = super(ModelUpdateView, self).get_context_data(**kwargs)
        context['back_url'] = back_url

        return context


class BinaDeleteView(DeleteView):
    model = Bina
    success_url = reverse_lazy('app:bina-list')


class DaireDeleteView(DeleteView):
    model = Daire

    def dispatch(self, request, *args, **kwargs):
        daire = Daire.objects.get(pk=self.kwargs['pk'])
        self.success_url = reverse_lazy('app:daire-list', kwargs={'bina_slug': daire.bina.slug})
        return super(DaireDeleteView, self).dispatch(request, *args, **kwargs)


class OdaDeleteView(DeleteView):
    model = Oda

    def dispatch(self, request, *args, **kwargs):
        oda = Oda.objects.get(pk=self.kwargs['pk'])
        self.success_url = reverse_lazy('app:oda-list', kwargs={'bina_slug': oda.daire.bina.slug,
                                                                  'daire_pk': oda.daire.pk})
        return super(OdaDeleteView, self).dispatch(request, *args, **kwargs)


class EsyaDeleteView(DeleteView):
    model = Esya

    def dispatch(self, request, *args, **kwargs):
        esya = Esya.objects.get(pk=self.kwargs['pk'])
        self.success_url = reverse_lazy('app:esya-list', kwargs={'bina_slug': esya.oda.daire.bina.slug,
                                                                  'daire_pk': esya.oda.daire.pk,
                                                                  'oda_slug': esya.oda.slug})
        return super(EsyaDeleteView, self).dispatch(request, *args, **kwargs)

