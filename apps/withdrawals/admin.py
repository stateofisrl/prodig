"""
Withdrawals admin configuration.
"""

from django.contrib import admin
from django.utils import timezone
from .models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'cryptocurrency', 'status', 'created_at']
    list_filter = ['status', 'cryptocurrency', 'created_at']
    search_fields = ['user__email', 'cryptocurrency', 'wallet_address']
    readonly_fields = ['user', 'amount', 'cryptocurrency', 'wallet_address', 'created_at']
    actions = ['mark_as_processing', 'mark_as_completed', 'mark_as_rejected']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Withdrawal Request', {
            'fields': ('user', 'amount', 'cryptocurrency', 'wallet_address', 'created_at')
        }),
        ('Processing', {
            'fields': ('status', 'transaction_hash', 'processed_by', 'processed_at')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
    )
    
    def mark_as_processing(self, request, queryset):
        """Mark withdrawals as processing."""
        count = queryset.filter(status='pending').update(status='processing')
        self.message_user(request, f'{count} withdrawal(s) marked as processing.')
    mark_as_processing.short_description = 'Mark as processing'
    
    def mark_as_completed(self, request, queryset):
        """Mark withdrawals as completed."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        count = 0
        for withdrawal in queryset.filter(status__in=['pending', 'processing']):
            withdrawal.status = 'completed'
            withdrawal.processed_at = timezone.now()
            withdrawal.processed_by = request.user
            withdrawal.save()
            
            # Deduct amount from user balance
            user = withdrawal.user
            if user.balance >= withdrawal.amount:
                user.balance -= withdrawal.amount
                user.save()
            
            count += 1
        
        self.message_user(request, f'{count} withdrawal(s) marked as completed.')
    mark_as_completed.short_description = 'Mark as completed'
    
    def mark_as_rejected(self, request, queryset):
        """Mark withdrawals as rejected."""
        count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{count} withdrawal(s) marked as rejected.')
    mark_as_rejected.short_description = 'Mark as rejected'
