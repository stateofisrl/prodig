"""
Referral serializers.
"""

from rest_framework import serializers
from .models import Referral, ReferralCommission, ReferralSettings
from apps.users.serializers import UserProfileSerializer


class ReferralSerializer(serializers.ModelSerializer):
    """Serializer for referral relationships."""
    
    referrer = UserProfileSerializer(read_only=True)
    referred = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReferralCommissionSerializer(serializers.ModelSerializer):
    """Serializer for referral commissions."""
    
    referrer_name = serializers.CharField(source='referral.referrer.username', read_only=True)
    referred_name = serializers.CharField(source='referral.referred.username', read_only=True)
    deposit_amount = serializers.DecimalField(
        source='deposit.amount',
        max_digits=15,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = ReferralCommission
        fields = [
            'id', 'referrer_name', 'referred_name', 'amount',
            'deposit_amount', 'status', 'created_at', 'paid_at'
        ]
        read_only_fields = ['id', 'created_at', 'paid_at']


class ReferralStatsSerializer(serializers.Serializer):
    """Serializer for referral statistics."""
    
    total_referrals = serializers.IntegerField()
    total_commissions_earned = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending_commissions = serializers.DecimalField(max_digits=15, decimal_places=2)
    paid_commissions = serializers.DecimalField(max_digits=15, decimal_places=2)
    referral_code = serializers.CharField()
    commission_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class ReferralSettingsSerializer(serializers.ModelSerializer):
    """Serializer for referral settings."""
    
    class Meta:
        model = ReferralSettings
        fields = [
            'commission_percentage',
            'is_active',
            'minimum_deposit_for_commission',
            'max_commission_amount'
        ]
