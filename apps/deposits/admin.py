"""
Deposits admin configuration.
"""

from django.contrib import admin
from django.utils import timezone
from .models import Deposit, CryptoWallet


@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency', 'wallet_address', 'is_active', 'created_at']
    list_filter = ['is_active', 'cryptocurrency']
    search_fields = ['cryptocurrency', 'wallet_address']
    ordering = ['cryptocurrency']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['user', 'cryptocurrency', 'amount', 'status', 'created_at']
    list_filter = ['status', 'cryptocurrency', 'created_at']
    search_fields = ['user__email', 'cryptocurrency']
    readonly_fields = ['user', 'cryptocurrency', 'amount', 'created_at', 'proof_content']
    actions = ['approve_deposit', 'reject_deposit']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User & Deposit Info', {
            'fields': ('user', 'cryptocurrency', 'amount', 'created_at')
        }),
        ('Proof Details', {
            'fields': ('proof_type', 'proof_content', 'proof_image')
        }),
        ('Status & Admin Actions', {
            'fields': ('status', 'admin_notes', 'approved_by', 'approved_at')
        }),
    )
    
    def approve_deposit(self, request, queryset):
        """Admin action to approve deposits."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        approved_count = 0
        for deposit in queryset.filter(status='pending'):
            deposit.status = 'approved'
            deposit.approved_at = timezone.now()
            deposit.approved_by = request.user
            deposit.save()
            
            # Update user balance
            user = deposit.user
            user.balance += deposit.amount
            user.save()
            
            approved_count += 1
        
        self.message_user(request, f'{approved_count} deposit(s) approved successfully.')
    
    approve_deposit.short_description = 'Approve selected deposits'
    
    def reject_deposit(self, request, queryset):
        """Admin action to reject deposits."""
        rejected_count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{rejected_count} deposit(s) rejected.')
    
    reject_deposit.short_description = 'Reject selected deposits'
