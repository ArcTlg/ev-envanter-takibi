# -*- coding: utf-8 -*-

from django.db import models
from django.utils.text import slugify


class Bina(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    total_price = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Bina, self).save()


class Daire(models.Model):
    bina = models.ForeignKey(Bina, on_delete=models.CASCADE)
    no = models.IntegerField()
    total_price = models.FloatField(default=0)

    def __unicode__(self):
        return "{} / Daire:{}".format(self.bina.name, self.no)


class Oda(models.Model):
    daire = models.ForeignKey(Daire, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    total_price = models.FloatField(default=0)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Oda, self).save()


class Esya(models.Model):
    oda = models.ForeignKey(Oda, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        self.oda.total_price += self.price
        self.oda.save()
        self.oda.daire.total_price += self.price
        self.oda.daire.save()
        self.oda.daire.bina.total_price += self.price
        self.oda.daire.bina.save()
        super(Esya, self).save()
