"""
Withdrawals serializers.
"""

from rest_framework import serializers
from .models import Withdrawal


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = [
            'id', 'user', 'amount', 'cryptocurrency', 'wallet_address',
            'status', 'transaction_hash', 'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'processed_at']


class CreateWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['amount', 'cryptocurrency', 'wallet_address']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Withdrawal amount must be greater than 0.')
        return value
    
    def validate_wallet_address(self, value):
        if not value or len(value) < 20:
            raise serializers.ValidationError('Invalid wallet address.')
        return value
