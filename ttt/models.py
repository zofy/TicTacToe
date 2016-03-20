from __future__ import unicode_literals
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    vs_comp = models.IntegerField(default=0)
    vs_player = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ', ' + self.password

class Score(models.Model):
    challenger = models.ForeignKey(Player, null=True, related_name='challenger')
    opponent = models.ForeignKey(Player, null=True, related_name='opponent')
    board_size = models.PositiveIntegerField(default=3)
    game_lenght = models.PositiveIntegerField(default=3)
    score = models.CharField(max_length=7)


class LoggedUser(models.Model):
    name = models.CharField(max_length=20)
