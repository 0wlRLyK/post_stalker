from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.utils import ProgrammingError
from django.utils.translation import gettext_lazy as _

from users.models import User, UserSettings, Award
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'ip', 'birthday', 'country',
                                         'state', 'signature', 'title', 'gender', 'rank', 'respect', 'banreason',
                                         'money', 'ico_num', 'chat_color',
                                         )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ("Снаряга", {'fields': ('slot1', 'slot2', 'slot3', 'addon1', 'addon2', 'addon3', 'ammo1', 'ammo2',
                                'upgrade1', 'upgrade2', 'upgrade3',
                                )}),
    )
    list_display = ['username', 'id', 'email', "valid_username", ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "id", "icon_admin"]


@admin.register(UserSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Створимо об'єкт за замовчуванням при першому сторінки SiteSettingsAdmin зі списком налаштувань
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # обов'язково оберніть завантаження і збереження SiteSettings в try catch,
        # Щоб можна було виконати створення міграцій бази даних
        try:
            UserSettings.load().save()
        except ProgrammingError:
            pass

    # забороняємо додавання нових налаштувань
    def has_add_permission(self, request, obj=None):
        return False

    # а також видалення існуючих
    def has_delete_permission(self, request, obj=None):
        return False
