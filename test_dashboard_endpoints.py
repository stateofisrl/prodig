#!/usr/bin/env python
"""Test all dashboard endpoints"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json

User = get_user_model()

# Get user and token
user = User.objects.get(email='user@example.com')
token = Token.objects.get(user=user)

print(f"Testing with user: {user.email}")
print(f"Token: {token.key}\n")

# Create API client with token
client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

endpoints = [
    ('/api/users/me/', 'User Profile'),
    ('/api/investments/my-investments/active_investments/', 'Active Investments'),
    ('/api/deposits/my_deposits/', 'My Deposits'),
]

for endpoint, name in endpoints:
    print(f"\n{'='*60}")
    print(f"Testing: {endpoint}")
    print(f"Description: {name}")
    print(f"{'='*60}")
    
    response = client.get(endpoint)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response (first 200 chars):")
        print(json.dumps(data, indent=2, default=str)[:200])
    else:
        print(f"Error: {response.content}")

print(f"\n✅ Endpoint tests complete!")
