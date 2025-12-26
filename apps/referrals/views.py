"""
Referral views and API endpoints.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from .models import Referral, ReferralCommission, ReferralSettings
from .serializers import (
    ReferralSerializer, 
    ReferralCommissionSerializer,
    ReferralStatsSerializer,
    ReferralSettingsSerializer
)


class ReferralViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing referrals."""
    
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return referrals made by the current user."""
        return Referral.objects.filter(referrer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get referral statistics for the current user."""
        user = request.user
        
        # Get all referrals made by user
        referrals = Referral.objects.filter(referrer=user)
        
        # Get commission statistics
        commissions = ReferralCommission.objects.filter(referral__referrer=user)
        
        pending = commissions.filter(status='pending').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        paid = commissions.filter(status='paid').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Get referral settings
        settings = ReferralSettings.objects.first()
        commission_percentage = settings.commission_percentage if settings else 0
        
        stats_data = {
            'total_referrals': referrals.count(),
            'total_commissions_earned': paid + pending,
            'pending_commissions': pending,
            'paid_commissions': paid,
            'referral_code': user.referral_code,
            'commission_percentage': commission_percentage
        }
        
        serializer = ReferralStatsSerializer(stats_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_referrals(self, request):
        """Get list of users referred by the current user."""
        referrals = self.get_queryset()
        serializer = self.get_serializer(referrals, many=True)
        return Response(serializer.data)


class ReferralCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing referral commissions."""
    
    serializer_class = ReferralCommissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return commissions for the current user."""
        return ReferralCommission.objects.filter(
            referral__referrer=self.request.user
        ).order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending commissions."""
        commissions = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(commissions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def paid(self, request):
        """Get paid commissions."""
        commissions = self.get_queryset().filter(status='paid')
        serializer = self.get_serializer(commissions, many=True)
        return Response(serializer.data)
