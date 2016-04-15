from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinLengthValidator


class PlayerManager(models.Manager):
    def create_player(self, name, password):
        player = Player(name=name, password=password)
        Score.objects.create_score(player)
        player.save()
        return player


class Player(models.Model):
    name = models.CharField(max_length=20, validators=[
        MinLengthValidator(1, message='Your name must consist of at least 1 character.')], primary_key=True)
    password = models.CharField(max_length=15, validators=[
        MinLengthValidator(6, message='Password must consist of at least 6 characters.')])

    objects = PlayerManager()

    def __str__(self):
        return self.name + ', ' + self.password


class ScoreManager(models.Manager):
    def create_score(self, player):
        score = Score(player=player)
        score.save()
        return score

    def save_result(self, player, result):
        sc = Score.objects.get(player=player)
        if result == 'winner':
            sc.wins += 1
        elif result == 'looser':
            sc.loses += 1
        sc.save()


class Score(models.Model):
    player = models.OneToOneField(Player)
    board_size = models.PositiveIntegerField(default=9)
    game_lenght = models.PositiveIntegerField(default=5)
    wins = models.PositiveIntegerField(default=0)
    loses = models.PositiveIntegerField(default=0)

    objects = ScoreManager()

    def __str__(self):
        return self.player.name + ', size: ' + str(self.board_size) + ', lenght; ' + str(self.game_lenght) + ', wins: ' + str(self.wins) + ', loses: ' + str(self.loses)


class MenuUserManager(models.Manager):
    def create_menu_user(self, name):
        user = MenuUser(name=name)
        user.save()
        return user

    def delete_menu_user(self, name):
        MenuUser.objects.get(name=name).delete()

    def delete_all_menu_users(self):
        MenuUser.objects.all().delete()


class MenuUser(models.Model):
    name = models.CharField(max_length=20)

    objects = MenuUserManager()