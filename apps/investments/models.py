"""
Investment models.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class InvestmentPlan(models.Model):
    """Investment plan model."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    roi_percentage = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(99999.99)],
        help_text='Enter ROI percentage (up to 99999.99%)'
    )
    duration_days = models.IntegerField()  # Duration in days
    minimum_investment = models.DecimalField(max_digits=15, decimal_places=2, default=100.00)
    maximum_investment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['roi_percentage']
        verbose_name = 'Investment Plan'
        verbose_name_plural = 'Investment Plans'
    
    def __str__(self):
        return f"{self.name} - {self.roi_percentage}% ROI"


class UserInvestment(models.Model):
    """User investment subscription model."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='subscriptions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    expected_return = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    earned = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Investment'
        verbose_name_plural = 'User Investments'
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
    
    def calculate_expected_return(self):
        """Calculate expected return based on ROI."""
        roi = self.plan.roi_percentage / Decimal('100')
        return self.amount * roi
    
    def save(self, *args, **kwargs):
        if not self.expected_return:
            self.expected_return = self.calculate_expected_return()
        super().save(*args, **kwargs)
