# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-08 05:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrewdatabase', '0010_auto_20160408_0413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grain',
            old_name='malt_type',
            new_name='grain_type',
        ),
    ]