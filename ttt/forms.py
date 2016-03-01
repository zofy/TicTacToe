from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=15)


