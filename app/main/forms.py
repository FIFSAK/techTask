from .models import File
from django import forms
from django.contrib.auth.models import User


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    password = forms.CharField(widget=forms.PasswordInput())
