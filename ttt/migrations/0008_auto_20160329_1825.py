# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-29 16:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttt', '0007_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1, message='Your name must consist of at least 1 character.')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(6, message='Password must consist of at least 6 characters.')]),
        ),
    ]