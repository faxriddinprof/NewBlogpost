from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserUpdateForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'location')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', 'location')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
