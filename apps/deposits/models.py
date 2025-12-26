"""
Deposits models.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CryptoWallet(models.Model):
    """Cryptocurrency wallet addresses (admin managed)."""
    
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('USDT', 'Tether'),
        ('USDC', 'USD Coin'),
        ('BNB', 'Binance Coin'),
        ('XRP', 'Ripple'),
        ('ADA', 'Cardano'),
    ]
    
    cryptocurrency = models.CharField(
        max_length=10, 
        choices=CRYPTO_CHOICES, 
        unique=True
    )
    wallet_address = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['cryptocurrency']
        verbose_name = 'Crypto Wallet'
        verbose_name_plural = 'Crypto Wallets'
    
    def __str__(self):
        return f"{self.cryptocurrency} - {self.wallet_address[:20]}..."


class Deposit(models.Model):
    """User deposit model."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    cryptocurrency = models.CharField(max_length=10, choices=CryptoWallet.CRYPTO_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=8)
    proof_type = models.CharField(
        max_length=20,
        choices=[
            ('transaction_id', 'Transaction ID'),
            ('screenshot', 'Screenshot'),
            ('note', 'Note'),
        ]
    )
    proof_content = models.TextField()  # Transaction ID, screenshot URL, or note
    proof_image = models.ImageField(upload_to='deposit_proofs/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_deposits'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
    
    def __str__(self):
        return f"{self.user.email} - {self.cryptocurrency} {self.amount}"
