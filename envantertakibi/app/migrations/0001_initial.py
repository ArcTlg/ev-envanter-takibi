# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-31 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('total_price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Daire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField()),
                ('total_price', models.FloatField(default=0)),
                ('bina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Bina')),
            ],
        ),
        migrations.CreateModel(
            name='Esya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Oda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('total_price', models.FloatField(default=0)),
                ('daire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Daire')),
            ],
        ),
        migrations.AddField(
            model_name='esya',
            name='oda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Oda'),
        ),
    ]
