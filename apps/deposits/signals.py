"""
Deposits signals.
"""

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Deposit


@receiver(pre_save, sender=Deposit)
def stash_old_deposit_state(sender, instance, **kwargs):
    """Cache the previous status/approved_at for post-save logic."""
    if not instance.pk:
        instance._old_status = None
        instance._old_approved_at = None
        return
    try:
        old_instance = Deposit.objects.get(pk=instance.pk)
        instance._old_status = old_instance.status
        instance._old_approved_at = old_instance.approved_at
    except Deposit.DoesNotExist:
        instance._old_status = None
        instance._old_approved_at = None


@receiver(post_save, sender=Deposit)
def handle_deposit_credit(sender, instance, created, **kwargs):
    """Credit balance when a deposit becomes approved (create or update)."""
    from django.db import transaction
    from django.db.models import F
    
    old_status = getattr(instance, '_old_status', None)
    old_approved_at = getattr(instance, '_old_approved_at', None)

    is_new_approval = (
        instance.status == 'approved' and
        (old_status != 'approved') and
        (old_approved_at is None)
    )

    if not is_new_approval:
        return

    # Use atomic transaction to avoid race conditions
    with transaction.atomic():
        # Use F expression to increment atomically
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.filter(pk=instance.user.pk).update(balance=F('balance') + instance.amount)
        
        # Stamp approval time if not set
        Deposit.objects.filter(pk=instance.pk, approved_at__isnull=True).update(approved_at=timezone.now())
        
    print(f"[SIGNAL] Credited {instance.amount} to user {instance.user.email} for deposit #{instance.pk}")


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
