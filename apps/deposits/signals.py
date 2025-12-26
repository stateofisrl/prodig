"""
Deposits signals.
"""

from django.db.models.signals import pre_save, post_save
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


@receiver(post_save, sender=Deposit)
def send_deposit_email(sender, instance, created, **kwargs):
    """Send email notification when deposit status changes or is created."""
    if created:
        # New deposit - notify admin
        try:
            from apps.users.emails import send_admin_deposit_notification
            print(f"[SIGNAL] Sending admin notification for new deposit #{instance.pk} - ${instance.amount}")
            send_admin_deposit_notification(instance)
            print(f"[SIGNAL] Admin email sent successfully for deposit #{instance.pk}")
        except Exception as e:
            print(f"[ERROR] Failed to send admin deposit email: {e}")
            import traceback
            traceback.print_exc()
    elif not created and instance.status in ['approved', 'rejected']:
        # Status changed - notify user
        try:
            from apps.users.emails import send_deposit_notification
            send_deposit_notification(instance)
        except Exception as e:
            print(f"Failed to send deposit email: {e}")
