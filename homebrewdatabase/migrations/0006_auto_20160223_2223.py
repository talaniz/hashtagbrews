# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-23 22:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrewdatabase', '0005_hop_origin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hop',
            old_name='origin',
            new_name='country',
        ),
    ]
