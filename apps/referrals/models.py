"""
Referral models for Investment Platform.
"""

from django.db import models
from django.conf import settings
import uuid


class ReferralSettings(models.Model):
    """Global referral settings managed by admin."""
    
    commission_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=5.00,
        help_text="Percentage commission on referred user's first deposit"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable entire referral system"
    )
    minimum_deposit_for_commission = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        help_text="Minimum deposit amount to earn commission"
    )
    max_commission_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        help_text="Maximum commission per referral (0 = unlimited)"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Referral Settings'
        verbose_name_plural = 'Referral Settings'
    
    def __str__(self):
        return f"Referral Settings - {self.commission_percentage}% commission"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and ReferralSettings.objects.exists():
            raise ValueError("Only one ReferralSettings instance is allowed")
        return super().save(*args, **kwargs)


class Referral(models.Model):
    """Track referral relationships between users."""
    
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referrals_made',
        help_text="User who referred someone"
    )
    referred = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral',
        help_text="User who was referred"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referred.username}"


class ReferralCommission(models.Model):
    """Track commission earned from referrals."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name='commissions'
    )
    deposit = models.ForeignKey(
        'deposits.Deposit',
        on_delete=models.CASCADE,
        related_name='referral_commissions'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Referral Commission'
        verbose_name_plural = 'Referral Commissions'
    
    def __str__(self):
        return f"${self.amount} commission for {self.referral.referrer.username}"
    
    def mark_as_paid(self):
        """Mark commission as paid and update user balance."""
        from django.utils import timezone
        if self.status != 'paid':
            self.status = 'paid'
            self.paid_at = timezone.now()
            
            # Add commission to referrer's balance
            referrer = self.referral.referrer
            referrer.balance += self.amount
            referrer.total_earnings += self.amount
            referrer.save()
            
            self.save()
            
            # Create transaction record
            CommissionTransaction.objects.create(
                commission=self,
                user=referrer,
                amount=self.amount,
                transaction_type='commission_paid'
            )


class CommissionTransaction(models.Model):
    """Track all commission-related transactions for user dashboard."""
    
    TRANSACTION_TYPES = [
        ('commission_earned', 'Commission Earned'),
        ('commission_paid', 'Commission Paid'),
        ('commission_cancelled', 'Commission Cancelled'),
    ]
    
    commission = models.ForeignKey(
        ReferralCommission,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commission_transactions'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20, 
        choices=TRANSACTION_TYPES, 
        default='commission_earned'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commission Transaction'
        verbose_name_plural = 'Commission Transactions'
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.transaction_type})"
