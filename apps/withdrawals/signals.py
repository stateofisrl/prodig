"""
Withdrawals signals.
"""

from django.db.models.signals import pre_save, post_save
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


@receiver(post_save, sender=Withdrawal)
def send_withdrawal_email(sender, instance, created, **kwargs):
    """Send email notification when withdrawal status changes or is created."""
    if created:
        # New withdrawal - notify admin
        try:
            from apps.users.emails import send_admin_withdrawal_notification
            print(f"[SIGNAL] Sending admin notification for new withdrawal #{instance.pk} - ${instance.amount}")
            send_admin_withdrawal_notification(instance)
            print(f"[SIGNAL] Admin email sent successfully for withdrawal #{instance.pk}")
        except Exception as e:
            print(f"[ERROR] Failed to send admin withdrawal email: {e}")
            import traceback
            traceback.print_exc()
    elif not created and instance.status in ['completed', 'rejected', 'processing']:
        # Status changed - notify user
        try:
            from apps.users.emails import send_withdrawal_notification
            send_withdrawal_notification(instance)
        except Exception as e:
            print(f"Failed to send withdrawal email: {e}")
