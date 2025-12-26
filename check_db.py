#!/usr/bin/env python
"""Check database data"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from apps.investments.models import InvestmentPlan, UserInvestment
from apps.deposits.models import CryptoWallet, Deposit
from apps.withdrawals.models import Withdrawal

User = get_user_model()

print("=" * 60)
print("DATABASE CHECK")
print("=" * 60)

# Users
print("\n1. USERS:")
for user in User.objects.all():
    token = Token.objects.filter(user=user).first()
    print(f"  - {user.email}: Balance=${user.balance}, Token={'✓' if token else '✗'}")

# Investment Plans
print("\n2. INVESTMENT PLANS:")
for plan in InvestmentPlan.objects.all():
    print(f"  - {plan.name}: {plan.roi_percentage}% ROI, Min: ${plan.minimum_investment}")

# User Investments
print("\n3. USER INVESTMENTS:")
for inv in UserInvestment.objects.all():
    print(f"  - {inv.user.email} -> {inv.plan.name}: ${inv.amount}")

# Crypto Wallets
print("\n4. CRYPTO WALLETS:")
for wallet in CryptoWallet.objects.all():
    print(f"  - {wallet.cryptocurrency}: {wallet.wallet_address}")

# Deposits
print("\n5. DEPOSITS:")
for deposit in Deposit.objects.all():
    print(f"  - {deposit.user.email}: ${deposit.amount} ({deposit.cryptocurrency})")

# Withdrawals
print("\n6. WITHDRAWALS:")
for withdrawal in Withdrawal.objects.all():
    print(f"  - {withdrawal.user.email}: ${withdrawal.amount} to {withdrawal.wallet_address}")

print("\n" + "=" * 60)
