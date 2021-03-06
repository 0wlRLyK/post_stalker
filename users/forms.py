from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User
from users.models_dir.funcs import Reputation
from users.models_dir.settings import UserSettings


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

    operation_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Действие")

    class Meta:
        model = Reputation
        fields = ['operation_type', 'subject']


class ChoiceImageColorForm(forms.Form):
    IMG_RANGE = UserSettings.load().ico_range_numbers
    IMAGES = [

        (f"{img}", f"/static/chats/icons/{img}.png") for img in range(IMG_RANGE.lower, IMG_RANGE.upper)
    ]
    COLORS = [
        ("#78866b", "#78866b"),
        ("#FF8C00", "#FF8C00"),
        ("orange", "orange"),
        ("#0000CD", "#0000CD"),
        ("#3c95af", "#3c95af"),
        ("#2f4532", "#2f4532"),
    ]
    ico = forms.ChoiceField(choices=IMAGES, widget=forms.RadioSelect, required=False)
    color = forms.ChoiceField(choices=COLORS, widget=forms.RadioSelect, required=False)


class SetStatus(forms.Form):
    status = forms.CharField(max_length=50, label="Новый статус: ")


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(max_length=150, required=True, label="Новое имя пользователя")


class EmptyForm(forms.Form):
    pass


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "birthday", "gender", "country", "state", "signature"]


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('avatar', 'x', 'y', 'width', 'height',)
