# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-16 06:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttt', '0014_auto_20160416_0736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='_loses',
        ),
        migrations.RemoveField(
            model_name='score',
            name='_wins',
        ),
    ]