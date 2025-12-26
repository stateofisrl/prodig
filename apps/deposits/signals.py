"""
Deposits signals.
"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Deposit


@receiver(pre_save, sender=Deposit)
def handle_deposit_approval(sender, instance, **kwargs):
    """
    Automatically credit user balance when deposit is approved.
    Uses status change detection and approved_at field to prevent duplicate credits.
    """
    if instance.pk:  # Only for existing deposits (updates)
        try:
            old_instance = Deposit.objects.get(pk=instance.pk)
            
            # CRITICAL: Only credit if status is ACTUALLY CHANGING from pending to approved
            # AND the deposit has not been credited before (approved_at is None)
            # This prevents duplicate credits on page refreshes or multiple saves
            if (old_instance.status != instance.status and
                old_instance.status == 'pending' and 
                instance.status == 'approved' and
                not old_instance.approved_at):
                # Credit the deposit amount to user balance
                instance.user.balance += instance.amount
                # Mark when it was approved to prevent future duplicates
                instance.approved_at = timezone.now()
                instance.user.save()
                
        except Deposit.DoesNotExist:
            pass
