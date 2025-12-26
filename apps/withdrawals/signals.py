"""
Withdrawals signals.
"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Withdrawal


@receiver(pre_save, sender=Withdrawal)
def handle_withdrawal_rejection(sender, instance, **kwargs):
    """
    Automatically refund user balance when withdrawal is rejected.
    Uses status change detection to prevent duplicate refunds.
    """
    if instance.pk:  # Only for existing withdrawals (updates)
        try:
            old_instance = Withdrawal.objects.get(pk=instance.pk)
            
            # CRITICAL: Only refund if status is ACTUALLY CHANGING to rejected
            # This prevents duplicate refunds on page refreshes or multiple saves
            if (old_instance.status != instance.status and
                old_instance.status in ['pending', 'processing'] and 
                instance.status == 'rejected'):
                # Refund the withdrawal amount back to user balance
                instance.user.balance += instance.amount
                instance.user.save()
                
        except Withdrawal.DoesNotExist:
            pass
