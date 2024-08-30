from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class MyUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "first_name", "last_name", "phone")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "pk",
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("pk", "email", "username", "first_name", "last_name", "phone")
    ordering = ("pk", "email", "username", "first_name")


admin.site.register(User, MyUserAdmin)
