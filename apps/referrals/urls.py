"""
URL configuration for referral app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReferralViewSet, ReferralCommissionViewSet

router = DefaultRouter()
router.register(r'referrals', ReferralViewSet, basename='referral')
router.register(r'commissions', ReferralCommissionViewSet, basename='referral-commission')

urlpatterns = [
    path('', include(router.urls)),
]
