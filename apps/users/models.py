"""
User models for Investment Platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class CustomUser(AbstractUser):
    """Extended User model with additional investment platform fields."""
    
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    referral_code = models.CharField(max_length=12, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Generate referral code if not exists
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the admin change URL for this user so admin 'View on site' links work."""
        from django.urls import reverse
        try:
            return reverse('admin:users_customuser_change', args=[self.pk])
        except Exception:
            return f'/admin/users/customuser/{self.pk}/change/'
