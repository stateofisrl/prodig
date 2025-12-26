#!/usr/bin/env python
"""Test API endpoints"""

import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from apps.investments.models import InvestmentPlan, UserInvestment
from apps.users.models import CustomUser

User = get_user_model()

# Get or create test user
user, created = User.objects.get_or_create(
    email='user@example.com',
    defaults={'first_name': 'Test', 'last_name': 'User'}
)

# Get token
token, _ = Token.objects.get_or_create(user=user)

print(f"User: {user.email}, Balance: {user.balance}, Total Invested: {user.total_invested}")
print(f"Token: {token.key}")

# Test API endpoints
BASE_URL = 'http://127.0.0.1:8000/api'
headers = {'Authorization': f'Token {token.key}'}

# 1. Test /api/users/me/
print("\n1. Testing /api/users/me/")
response = requests.get(f'{BASE_URL}/users/me/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 2. Test /api/investments/plans/
print("\n2. Testing /api/investments/plans/")
response = requests.get(f'{BASE_URL}/investments/plans/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 3. Test /api/investments/my-investments/
print("\n3. Testing /api/investments/my-investments/")
response = requests.get(f'{BASE_URL}/investments/my-investments/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 4. Test /api/deposits/wallets/
print("\n4. Testing /api/deposits/wallets/")
response = requests.get(f'{BASE_URL}/deposits/wallets/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 5. Test /api/withdrawals/
print("\n5. Testing /api/withdrawals/")
response = requests.get(f'{BASE_URL}/withdrawals/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n✅ All endpoints tested!")
