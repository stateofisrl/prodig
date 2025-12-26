"""
User admin configuration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    view_on_site = True
    list_display = [
        'email', 'username', 'first_name', 'last_name', 
        'balance', 'is_verified', 'created_at'
    ]
    list_filter = ['is_verified', 'created_at', 'is_staff']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('Investment Info', {'fields': ('balance', 'total_invested', 'total_earnings')}),
        ('Contact Info', {'fields': ('phone_number', 'country')}),
        ('Verification', {'fields': ('is_verified', 'verification_code')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    def get_view_on_site_url(self, obj=None):
        if obj is None:
            return None
        try:
            return obj.get_absolute_url()
        except Exception:
            return None
