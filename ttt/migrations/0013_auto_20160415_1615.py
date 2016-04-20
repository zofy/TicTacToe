# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-15 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ttt', '0012_auto_20160414_1721'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LoggedUser',
            new_name='MenuUser',
        ),
        migrations.RemoveField(
            model_name='player',
            name='vs_comp',
        ),
        migrations.RemoveField(
            model_name='player',
            name='vs_player',
        ),
        migrations.AlterField(
            model_name='score',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ttt.Player'),
        ),
    ]