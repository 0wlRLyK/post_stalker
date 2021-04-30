from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.db.utils import ProgrammingError
from django.utils.translation import gettext_lazy as _

from users import models as users_models
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = users_models.User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'ip', 'birthday', 'country',
                                         'state', 'signature', 'title', 'gender', 'rank', 'respect', 'banreason',
                                         'money', 'ico_num', 'chat_color', "equip"
                                         )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ['username', 'id', 'email', "valid_username", ]


admin.site.unregister(users_models.User)
admin.site.register(users_models.User, CustomUserAdmin)


@admin.register(users_models.Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "id", "icon_admin"]


@admin.register(users_models.UserSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Створимо об'єкт за замовчуванням при першому сторінки SiteSettingsAdmin зі списком налаштувань
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # обов'язково оберніть завантаження і збереження SiteSettings в try catch,
        # Щоб можна було виконати створення міграцій бази даних
        try:
            users_models.UserSettings.load().save()
        except ProgrammingError:
            pass

    # забороняємо додавання нових налаштувань
    def has_add_permission(self, request, obj=None):
        return False

    # а також видалення існуючих
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(users_models.Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.Pistol)
class PistolAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.Ammo)
class AmmoAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.PistolAmmo)
class PistolAmmoAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.Grenade)
class GrenadeAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.UpgradeWeapon)
class UpgradeWeaponAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.UpgradeOutfit)
class UpgradeOutfitAdmin(admin.ModelAdmin):
    list_display = ["name", "icon_admin", "cost"]


@admin.register(users_models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["id"]


class GroupInline(admin.StackedInline):
    model = users_models.Fraction
    can_delete = False
    verbose_name_plural = "Группировки"
    verbose_name = "Группировка"


class GroupAdmin(GroupAdmin):
    inlines = (GroupInline,)


# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
