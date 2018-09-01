# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Bina, Daire, Oda, Esya


def index(request):
    binalar = Bina.objects.all()
    context = {'binalar': binalar}
    if request.method == 'POST' and 'delete_item' in request.POST:
        pk = request.POST.get('delete_item')
        obj = Bina.objects.get(pk=pk)
        obj.delete()

    return render(request, 'app/index.html', context)


def bina_ekle(request):
    context = {'panel_title': 'Yeni Bina Kaydi',
               'input_name': 'Bina Ismi',
               'button_id_name': 'yeni_bina',
               'button_name': 'Ekle',
               'input_value_name': '',
               'request': request}

    if request.method == 'POST' and 'yeni_bina' in request.POST:
        val = request.POST.get('input_val')
        if val:
            bina = Bina()
            bina.name = val
            bina.save()
            return HttpResponseRedirect(reverse('app:index'))
        else:
            context['panel_title'] = 'Hata'
            return render(request, 'app/add_edit_page.html', context)
    else:
        return render(request, 'app/add_edit_page.html', context)


def bina(request, bina_slug):
    selected_bina = Bina.objects.get(slug=bina_slug)
    daireler = Daire.objects.filter(bina=selected_bina)
    context = {'daireler': daireler,
               'bina': selected_bina}

    if request.method == 'POST' and 'delete_item' in request.POST:
        pk = request.POST.get('delete_item')
        obj = Daire.objects.get(pk=pk)
        obj.delete()

    return render(request, 'app/bina.html', context)


def daire_ekle(request, bina_slug):
    context = {'panel_title': 'Yeni Daire Kaydi',
               'input_name': 'Daire No',
               'button_id_name': 'yeni_daire',
               'button_name': 'Ekle',
               'input_value_name': '',
               'request': request}

    if request.method == 'POST' and 'yeni_daire' in request.POST:
        val = request.POST.get('input_val')
        if val:
            bina = Bina.objects.get(slug=bina_slug)
            daire = Daire()
            daire.bina = bina
            daire.no = int(val)
            daire.save()
            return HttpResponseRedirect(reverse('app:bina', args=(bina_slug,)))
        else:
            context['panel_title'] = 'Hata'
            return render(request, 'app/add_edit_page.html', context)
    else:
        return render(request, 'app/add_edit_page.html', context)


def daire(request, bina_slug, pk):
    selected_bina = Bina.objects.get(slug=bina_slug)
    selected_daire = Daire.objects.get(bina=selected_bina, pk=pk)
    odalar = Oda.objects.filter(daire=selected_daire)
    context = {'odalar': odalar,
               'daire': selected_daire,
               'bina': selected_bina}

    if request.method == 'POST' and 'delete_item' in request.POST:
        pk = request.POST.get('delete_item')
        obj = Daire.objects.get(bina=selected_bina, pk=pk)
        obj.delete()

    return render(request, 'app/daire.html', context)


def oda_ekle(request, bina_slug, pk):
    context = {'panel_title': 'Yeni Oda Kaydi',
               'input_name': 'Oda Adi',
               'button_id_name': 'yeni_oda',
               'button_name': 'Ekle',
               'input_value_name': '',
               'request': request}

    if request.method == 'POST' and 'yeni_oda' in request.POST:
        val = request.POST.get('input_val')
        if val:
            daire_obj = Daire.objects.get(bina__slug=bina_slug, pk=pk)
            oda = Oda()
            oda.daire = daire_obj
            oda.name = val
            oda.save()
            return HttpResponseRedirect(reverse('app:daire', args=(bina_slug, pk)))
        else:
            context['panel_title'] = 'Hata'
            return render(request, 'app/add_edit_page.html', context)
    else:
        return render(request, 'app/add_edit_page.html', context)


def oda(request, bina_slug, pk, oda_slug):
    selected_bina = Bina.objects.get(slug=bina_slug)
    selected_daire = Daire.objects.get(bina=selected_bina, pk=pk)
    selected_oda = Oda.objects.get(slug=oda_slug, daire=selected_daire)
    esyalar = Esya.objects.filter(oda=selected_oda)
    context = {'esyalar': esyalar,
               'daire': selected_daire,
               'bina': selected_bina,
               'oda': selected_oda}

    if request.method == 'POST' and 'delete_item' in request.POST:
        pk = request.POST.get('delete_item')
        obj = Esya.objects.get(pk=pk)
        obj.delete()
    elif request.method == 'POST' and 'edit_item' in request.POST:
        selected_esya = Esya.objects.get(oda=selected_oda, pk=pk)
        context = {'panel_title': 'Yeni Esya Kaydi',
                   'input_name': 'Esya Adi',
                   'button_id_name': 'yeni_esya',
                   'button_name': 'Ekle',
                   'input_value_name': selected_esya.name}
        return render(request, 'app/add_edit_page.html', context)
    return render(request, 'app/oda.html', context)


def esya_ekle(request, bina_slug, pk, oda_slug):
    context = {'panel_title': 'Yeni Esya Kaydi',
               'input_name': 'Esya Adi',
               'button_id_name': 'yeni_esya',
               'button_name': 'Ekle',
               'input_value_name': '',
               'request': request}
    print(request.POST)
    if request.method == 'POST' and 'yeni_esya' in request.POST:
        val = request.POST.get('input_val')
        if val:
            selected_daire = Daire.objects.get(bina__slug=bina_slug, pk=pk)
            oda_obj = Oda.objects.get(daire=selected_daire, slug=oda_slug)
            esya = Esya()
            esya.oda = oda_obj
            esya.name = val
            esya.price = 1000
            esya.save()
            return HttpResponseRedirect(reverse('app:oda', args=(bina_slug, pk, oda_slug)))
        else:
            context['panel_title'] = 'Hata'
            return render(request, 'app/add_edit_page.html', context)
    else:
        return render(request, 'app/add_edit_page.html', context)


