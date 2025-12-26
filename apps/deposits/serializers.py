"""
Deposits serializers.
"""

from rest_framework import serializers
from .models import Deposit, CryptoWallet


class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = ['id', 'cryptocurrency', 'wallet_address', 'is_active']


class DepositSerializer(serializers.ModelSerializer):
    wallet_address = serializers.SerializerMethodField(read_only=True)

    def get_wallet_address(self, obj):
        try:
            wallet = CryptoWallet.objects.filter(cryptocurrency=obj.cryptocurrency, is_active=True).first()
            return wallet.wallet_address if wallet else None
        except Exception:
            return None
    class Meta:
        model = Deposit
        fields = [
            'id', 'user', 'cryptocurrency', 'amount', 'proof_type',
            'proof_content', 'proof_image', 'status', 'created_at', 'approved_at', 'wallet_address'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'approved_at']


class CreateDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['cryptocurrency', 'amount', 'proof_type', 'proof_content', 'proof_image']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Deposit amount must be greater than 0.')
        return value
