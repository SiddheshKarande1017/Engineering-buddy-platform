from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Problem, Sources
from django import forms
from django.forms import ModelForm
from django.db import models
from django import forms
from .models import UploadedDoc


class UploadDocForm(forms.ModelForm):
    class Meta:
        model = UploadedDoc
        fields = ('doc_file',)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class Addproblem(forms.Form):
    topic = forms.CharField(max_length=30)
    q_name = forms.CharField(max_length=30)
    link = forms.URLField(max_length=200)


class Addtopic(forms.Form):
    topic = forms.CharField(max_length=30)
    link = forms.URLField(max_length=200)
