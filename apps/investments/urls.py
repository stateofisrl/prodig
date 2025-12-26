"""
Investment URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestmentPlanViewSet, UserInvestmentViewSet

router = DefaultRouter()
router.register(r'plans', InvestmentPlanViewSet, basename='plan')
router.register(r'my-investments', UserInvestmentViewSet, basename='user-investment')

urlpatterns = [
    path('', include(router.urls)),
]
