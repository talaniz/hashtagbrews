# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-23 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrewdatabase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hop',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
