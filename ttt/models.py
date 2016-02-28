from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import CharField
from pygments.lexers.jvm import ScalaLexer


class Player(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.name + ',' + self.password


class Score(models.Model):
    vs_comp = models.IntegerField(default=0)
    vs_player = models.IntegerField(default=0)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


