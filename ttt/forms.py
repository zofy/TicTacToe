from django import forms
from django.forms import ModelForm

from models import Player


class LoginForm(ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'password')
        labels = {
            'name': 'Username',
            'password': 'Password'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'password'})
        }


class RegisterForm(LoginForm):
    confirmPassword = forms.CharField(label='Confirm password',
                                      widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
                                      max_length=15,
                                      min_length=6)

    def clean(self):
        p = self.cleaned_data.get('password')
        cp = self.cleaned_data.get('confirmPassword')
        if p != cp:
            raise forms.ValidationError('Passwords do not match!')
        # return self.cleaned_data
