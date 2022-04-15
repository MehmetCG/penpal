from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username", 
        "email", 
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


admin.site.register(User, UserAdmin)