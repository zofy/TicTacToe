from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import CharField


class player(models.Model):
    name = models.CharField(max_length=200)