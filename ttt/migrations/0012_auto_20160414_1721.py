# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-14 15:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttt', '0011_auto_20160414_1455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='name',
            new_name='player',
        ),
    ]
