from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinLengthValidator


class Player(models.Model):
    name = models.CharField(max_length=20, validators=[
        MinLengthValidator(1, message='Your name must consist of at least 1 character.')], primary_key=True)
    password = models.CharField(max_length=15, validators=[
        MinLengthValidator(6, message='Password must consist of at least 6 characters.')])
    vs_comp = models.IntegerField(default=0)
    vs_player = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ', ' + self.password


class Score(models.Model):
    player = models.ForeignKey(Player)
    board_size = models.PositiveIntegerField(default=9)
    game_lenght = models.PositiveIntegerField(default=5)
    wins = models.PositiveIntegerField(default=0)
    loses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.player.name + ', size: ' + str(self.board_size) + ', lenght; ' + str(self.game_lenght) + ', wins: ' + str(self.wins) + ', loses: ' + str(self.loses)


class LoggedUser(models.Model):
    name = models.CharField(max_length=20)
