from django import forms
from models import Player


class RegisterForm(forms.Form):
    class Meta:
        model = Player
        # fields = ('name', 'password')
