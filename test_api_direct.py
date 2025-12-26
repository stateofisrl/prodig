#!/usr/bin/env python
"""Direct API test without going through network"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

# Get user and token
user = User.objects.get(email='user@example.com')
token = Token.objects.get(user=user)

print(f"Testing with user: {user.email}")
print(f"Token: {token.key}")
print(f"User Balance: {user.balance}")
print(f"User Total Invested: {user.total_invested}")
print(f"User Total Earnings: {user.total_earnings}")

# Create API client
client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

print("\n" + "="*60)
print("Testing /api/users/me/")
print("="*60)

response = client.get('/api/users/me/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Response keys: {list(data.keys())}")
    print(f"Balance in response: {data.get('balance')}")
    print(f"Total Invested in response: {data.get('total_invested')}")
    print(f"Total Earnings in response: {data.get('total_earnings')}")
else:
    print(f"Error: {response.content}")

print("\n" + "="*60)
print("Testing /api/investments/my-investments/active_investments/")
print("="*60)

response = client.get('/api/investments/my-investments/active_investments/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Response: {data}")
else:
    print(f"Error: {response.content}")

print("\n" + "="*60)
print("Testing /api/investments/plans/")
print("="*60)

response = client.get('/api/investments/plans/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if isinstance(data, dict) and 'results' in data:
        print(f"Plans (paginated): {len(data['results'])} results")
        for plan in data['results']:
            print(f"  - {plan['name']}: ROI {plan['roi_percentage']}%")
    else:
        print(f"Plans: {data}")
else:
    print(f"Error: {response.content}")

print("\n✅ API Test Complete")
