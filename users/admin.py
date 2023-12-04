from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'is_authenticated')

    def is_authenticated(self, obj):
        return obj.is_authenticated
    is_authenticated.boolean = True
    is_authenticated.short_description = 'Authenticated'

    ordering = ('email',)
