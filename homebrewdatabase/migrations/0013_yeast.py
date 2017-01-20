# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-02 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrewdatabase', '0012_auto_20160408_0534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yeast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('lab', models.CharField(choices=[('Brewferm', 'Brewferm'), ('Brewtek', 'Brewtek'), ('Coopers', 'Coopers'), ('Danstar', 'Danstar'), ('DCL/Fermentis', 'DCL/Fermentis'), ('Doric', 'Doric'), ('East Coast Yeast', 'East Coast Yeast'), ('Edme', 'Edme'), ('Glenbrew', 'Glenbrew'), ('Lallemend', 'Lallemend'), ('Munton Fison', 'Munton Fison'), ('Red Star', 'Red Star'), ('Wyeast', 'Wyeast'), ('Wylabs', 'Wylabs'), ('Yeast Bay', 'The Yeast Bay')], default='Wylabs', max_length=20)),
                ('yeast_type', models.CharField(choices=[('Ale', 'Ale'), ('Champagne', 'Champagne'), ('Lager', 'Lager'), ('Wheat', 'Wheat'), ('Wine', 'Wine')], default='Ale', max_length=15)),
                ('yeast_form', models.CharField(choices=[('Liquid', 'Liquid'), ('Dry', 'Dry')], default='Liquid', max_length=10)),
                ('min_temp', models.IntegerField()),
                ('max_temp', models.IntegerField()),
                ('attenuation', models.IntegerField()),
                ('flocculation', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Very High', 'Very high')], default='Medium', max_length=15)),
                ('comments', models.TextField()),
            ],
        ),
    ]
