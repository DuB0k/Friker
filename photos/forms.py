# -*- coding: utf-8 -*-
from django import forms
from models import Photo


class LoginForm(forms.Form):

    user_username = forms.CharField(label='Nombre de usuario')
    user_password = forms.CharField(label='Password', widget=forms.PasswordInput)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo