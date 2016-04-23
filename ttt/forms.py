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

    def clean(self):
        return self.cleaned_data

    def authenticate(self):
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        try:
            return Player.objects.get(name=name, password=password)
        except:
            return None


class RegisterForm(LoginForm):
    confirmPassword = forms.CharField(label='Confirm password',
                                      widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
                                      max_length=15,
                                      min_length=6)

    def clean(self):
        name = self.cleaned_data.get('name')
        if Player.objects.filter(name=name).exists():
            raise forms.ValidationError('Name ' + name + ' already exists, try another one!')
        p = self.cleaned_data.get('password')
        cp = self.cleaned_data.get('confirmPassword')
        if p != cp and (p and cp is not None):
            raise forms.ValidationError('Passwords do not match!')
        return self.cleaned_data
