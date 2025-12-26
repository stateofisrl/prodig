"""
Withdrawals models.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Withdrawal(models.Model):
    """User withdrawal request model."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    cryptocurrency = models.CharField(
        max_length=10,
        choices=[
            ('BTC', 'Bitcoin'),
            ('ETH', 'Ethereum'),
            ('USDT', 'Tether'),
            ('USDC', 'USD Coin'),
            ('BNB', 'Binance Coin'),
            ('XRP', 'Ripple'),
            ('ADA', 'Cardano'),
        ]
    )
    wallet_address = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    transaction_hash = models.CharField(max_length=200, blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_withdrawals'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Withdrawal'
        verbose_name_plural = 'Withdrawals'
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.cryptocurrency}"
