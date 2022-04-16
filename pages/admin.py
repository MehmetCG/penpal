from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email",),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "age",
        "gender",
        "country", 
        "native_language", 
        "practising_language",
    )
    list_filter = (
        "age", 
        "gender", 
        "country", 
        "native_language", 
        "practising_language",
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)