"""
Investment serializers.
"""

from rest_framework import serializers
from .models import InvestmentPlan, UserInvestment


class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = [
            'id', 'name', 'description', 'roi_percentage', 
            'duration_days', 'minimum_investment', 'maximum_investment', 'is_active'
        ]
        read_only_fields = ['id']


class UserInvestmentSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_roi = serializers.DecimalField(
        source='plan.roi_percentage', 
        max_digits=7, 
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = UserInvestment
        fields = [
            'id', 'user', 'plan', 'plan_name', 'plan_roi', 'amount',
            'status', 'start_date', 'end_date', 'expected_return',
            'earned', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'expected_return', 'earned', 'created_at']


class CreateUserInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvestment
        fields = ['plan', 'amount']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Investment amount must be greater than 0.')
        return value
    
    def validate(self, attrs):
        plan = attrs['plan']
        amount = attrs['amount']
        
        if amount < plan.minimum_investment:
            raise serializers.ValidationError(
                f'Minimum investment for this plan is {plan.minimum_investment}'
            )
        
        if plan.maximum_investment and amount > plan.maximum_investment:
            raise serializers.ValidationError(
                f'Maximum investment for this plan is {plan.maximum_investment}'
            )
        
        if not plan.is_active:
            raise serializers.ValidationError('This plan is not currently active.')
        
        return attrs
