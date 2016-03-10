from __future__ import unicode_literals
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    vs_comp = models.IntegerField(default=0)
    vs_player = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ',' + self.password


class LoggedUser(models.Model):
    name = models.CharField(max_length=20)
