#!/usr/bin/env python
"""Test API with requests"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import json

User = get_user_model()

# Get user token
user = User.objects.get(email='user@example.com')
token = Token.objects.get(user=user)

print(f"Testing API with token: {token.key}")
print(f"User: {user.email}, Balance: {user.balance}")

# Test with requests
import requests

BASE_URL = 'http://127.0.0.1:8000/api'
headers = {
    'Authorization': f'Token {token.key}',
    'Content-Type': 'application/json'
}

print("\n" + "="*60)
print("Testing /api/users/me/")
print("="*60)

response = requests.get(f'{BASE_URL}/users/me/', headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Response Text: {response.text[:500]}")

if response.status_code == 200:
    data = response.json()
    print(f"\nParsed JSON:")
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code}")
