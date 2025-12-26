"""
Deposits URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, CryptoWalletViewSet

router = DefaultRouter()
router.register(r'wallets', CryptoWalletViewSet, basename='wallet')
router.register(r'', DepositViewSet, basename='deposit')

urlpatterns = [
    path('', include(router.urls)),
]
