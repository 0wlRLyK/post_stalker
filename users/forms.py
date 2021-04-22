from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Reputation


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class AddRepForm(forms.ModelForm):
    CHOICES = [('null', 'не изменять репутацию'),
               ('plus', 'повысить репутацию'),
               ('minus', 'понизить репутацию')]

    operation_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Reputation
        fields = ['subject', 'operation_type']
