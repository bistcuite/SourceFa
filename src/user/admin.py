from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username',]

    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('website','twitter','name','company','bio','position',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)