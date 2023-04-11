from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", 'phone', 'first_name', 'last_name', "is_staff", "is_active",)
    list_filter = ("email", 'phone', "is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "password", 'phone', 'first_name', 'last_name')}),
        ("Permissions", {"fields": ("is_staff", "is_active",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", 'phone', 'first_name', 'last_name', "password1", "password2", "is_staff",
            )}
        ),
    )
    search_fields = ("email", 'phone',)
    ordering = ("email", 'phone',)



admin.site.register(CustomUser, CustomUserAdmin)