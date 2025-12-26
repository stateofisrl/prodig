"""
Signals for referral app - automatically create commissions when deposits are approved.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.deposits.models import Deposit
from .models import Referral, ReferralCommission, ReferralSettings, CommissionTransaction
from django.utils import timezone


@receiver(post_save, sender=Deposit)
def create_referral_commission(sender, instance, created, **kwargs):
    """
    Create referral commission when a deposit is approved.
    Only creates commission for the first deposit of a referred user.
    """
    # Only process when deposit is approved
    if instance.status != 'approved':
        return
    
    # Check if referral system is active
    try:
        settings = ReferralSettings.objects.first()
        if not settings or not settings.is_active:
            return
    except ReferralSettings.DoesNotExist:
        return
    
    # Check if user was referred
    try:
        referral = Referral.objects.get(referred=instance.user)
    except Referral.DoesNotExist:
        return
    
    # Check if commission already exists for this deposit
    if ReferralCommission.objects.filter(deposit=instance).exists():
        return
    
    # Check minimum deposit requirement
    if instance.amount < settings.minimum_deposit_for_commission:
        return
    
    # Calculate commission
    commission_amount = (instance.amount * settings.commission_percentage) / 100
    
    # Apply max commission limit if set
    if settings.max_commission_amount > 0:
        commission_amount = min(commission_amount, settings.max_commission_amount)
    
    # Create commission record
    ReferralCommission.objects.create(
        referral=referral,
        deposit=instance,
        amount=commission_amount,
        status='pending'
    )
    
    print(f"[REFERRAL] Created commission of ${commission_amount} for {referral.referrer.username}")


@receiver(pre_save, sender=ReferralCommission)
def handle_commission_status_change(sender, instance: ReferralCommission, **kwargs):
    """Credit user balance and create transaction when commission is marked paid.
    This covers cases where admins change status in the change form directly.
    """
    # Only process updates, not initial creation
    if not instance.pk:
        return
    try:
        previous = ReferralCommission.objects.get(pk=instance.pk)
    except ReferralCommission.DoesNotExist:
        return
    # Trigger only on transition to 'paid'
    if previous.status != 'paid' and instance.status == 'paid':
        referrer = instance.referral.referrer
        # Ensure paid_at is set
        if instance.paid_at is None:
            instance.paid_at = timezone.now()
        # Avoid double-crediting: check if a paid transaction already exists
        already_recorded = CommissionTransaction.objects.filter(
            commission=instance,
            transaction_type='commission_paid'
        ).exists()
        if not already_recorded:
            # Credit balances
            referrer.balance += instance.amount
            referrer.total_earnings += instance.amount
            referrer.save(update_fields=['balance', 'total_earnings'])
            # Create transaction record
            CommissionTransaction.objects.create(
                commission=instance,
                user=referrer,
                amount=instance.amount,
                transaction_type='commission_paid'
            )
