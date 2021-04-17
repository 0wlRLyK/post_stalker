from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'ip', 'birthday', 'country',
                                         'state', 'signature', 'title', 'gender', 'rank', 'respect', 'banreason',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ("Снаряга", {'fields': ('slot1', 'slot2', 'slot3', 'addon1', 'addon2', 'addon3', 'ammo1', 'ammo2',
                                'upgrade1', 'upgrade2', 'upgrade3',
                                )}),
    )
    list_display = ['username', 'id', 'email', ]
