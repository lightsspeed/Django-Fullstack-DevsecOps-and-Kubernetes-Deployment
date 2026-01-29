from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_verified', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'bio', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'bio', 'is_verified')}),
    )
