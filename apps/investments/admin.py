"""
Investment admin configuration.
"""

from django.contrib import admin
from .models import InvestmentPlan, UserInvestment


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'roi_percentage', 'duration_days', 'minimum_investment', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['roi_percentage']


@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'amount', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'plan', 'created_at']
    search_fields = ['user__email', 'plan__name']
    readonly_fields = ['user', 'plan', 'amount', 'start_date', 'expected_return']
    ordering = ['-created_at']
