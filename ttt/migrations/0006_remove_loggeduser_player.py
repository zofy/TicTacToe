# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-10 18:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttt', '0005_auto_20160310_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loggeduser',
            name='player',
        ),
    ]
