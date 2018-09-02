# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify


class Bina(models.Model):
    name = models.CharField('Bina Adi', max_length=100, unique=True)
    slug = models.SlugField(max_length=50)
    total_price = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:bina-list')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Bina, self).save()


class Daire(models.Model):
    bina = models.ForeignKey(Bina, on_delete=models.CASCADE)
    no = models.IntegerField('Daire No')
    total_price = models.FloatField(default=0)

    def __unicode__(self):
        return "%s / Daire:%s" % (self.bina.name, self.no)

    def get_absolute_url(self):
        return reverse('app:daire-list', kwargs={'bina_slug': self.bina.slug})


class Oda(models.Model):
    daire = models.ForeignKey(Daire, on_delete=models.CASCADE)
    name = models.CharField('Oda Adi', max_length=100)
    slug = models.SlugField(max_length=50)
    total_price = models.FloatField(default=0)

    def __unicode__(self):
        return '%s / %s' % (self.daire, self.name)

    def get_absolute_url(self):
        return reverse('app:oda-list', kwargs={'bina_slug': self.daire.bina.slug,
                                               'daire_pk': self.daire.pk})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Oda, self).save()


class Esya(models.Model):
    oda = models.ForeignKey(Oda, on_delete=models.CASCADE)
    name = models.CharField('Esya Adi', max_length=100)
    price = models.FloatField('Fiyat')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:esya-list', kwargs={'bina_slug': self.oda.daire.bina.slug,
                                                'daire_pk': self.oda.daire.pk,
                                                'oda_slug': self.oda.slug})


def calculate_total_price(sender, instance, **kwargs):

    if instance.pk:
        old_obj = sender.objects.get(pk=instance.pk)
        old_price = old_obj.price
        new_price = instance.price - old_price
    else:
        new_price = instance.price

    instance.oda.total_price += new_price
    instance.oda.save()

    instance.oda.daire.total_price += new_price
    instance.oda.daire.save()

    instance.oda.daire.bina.total_price += new_price
    instance.oda.daire.bina.save()


pre_save.connect(calculate_total_price, sender=Esya)
