from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User, Reputation, UserSettings


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


class ChoiceImageColorForm(forms.Form):
    IMG_RANGE = UserSettings.load().ico_range_numbers
    IMAGES = [

        (f"{img}", f"/static/post_stalker/ico/Chat/{img}.png") for img in range(IMG_RANGE.lower, IMG_RANGE.upper)
    ]
    COLORS = [
        ("green", "green"),
        ("red", "red"),
        ("yellow", "yellow"),
    ]
    ico = forms.ChoiceField(choices=IMAGES, widget=forms.RadioSelect, required=False)
    color = forms.ChoiceField(choices=COLORS, widget=forms.RadioSelect, required=False)


class SetStatus(forms.Form):
    status = forms.CharField(max_length=50, label="Новый статус: ")


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(max_length=150, required=True)
