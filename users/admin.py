from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    """Admin settings for custom User model, behaving like Django's default UserAdmin."""
    
    model = User

    # Add the custom "role" field to the UserAdmin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2"),
        }),
    )

    list_display = ("username", "email", "role", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
