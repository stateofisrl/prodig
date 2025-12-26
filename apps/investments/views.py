"""
Investment views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta
from decimal import Decimal
from .models import InvestmentPlan, UserInvestment
from .serializers import (
    InvestmentPlanSerializer, UserInvestmentSerializer,
    CreateUserInvestmentSerializer
)


class InvestmentPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Investment plan viewset - read only for users."""
    queryset = InvestmentPlan.objects.filter(is_active=True)
    serializer_class = InvestmentPlanSerializer
    permission_classes = [AllowAny]


class UserInvestmentViewSet(viewsets.ModelViewSet):
    """User investment viewset."""
    serializer_class = UserInvestmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserInvestmentSerializer
        return UserInvestmentSerializer
    
    @action(detail=False, methods=['get'])
    def my_investments(self, request):
        """Get all user investments."""
        investments = self.get_queryset()
        serializer = self.get_serializer(investments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active_investments(self, request):
        """Get only active investments."""
        investments = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(investments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Subscribe to an investment plan."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            plan = serializer.validated_data['plan']
            amount = serializer.validated_data['amount']
            
            # Check if user has sufficient balance
            if request.user.balance < amount:
                return Response(
                    {'detail': 'Insufficient balance. Please deposit funds.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create investment
            end_date = timezone.now() + timedelta(days=plan.duration_days)
            investment = UserInvestment.objects.create(
                user=request.user,
                plan=plan,
                amount=amount,
                end_date=end_date
            )
            
            # Deduct amount from user balance
            request.user.balance -= amount
            request.user.total_invested += amount
            request.user.save()
            
            return Response({
                'message': 'Investment created successfully',
                'investment': UserInvestmentSerializer(investment).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get investment statistics."""
        investments = self.get_queryset()
        active = investments.filter(status='active').count()
        completed = investments.filter(status='completed').count()
        total_amount = sum(inv.amount for inv in investments)
        total_earned = sum(inv.earned for inv in investments)
        
        return Response({
            'active_investments': active,
            'completed_investments': completed,
            'total_invested': str(total_amount),
            'total_earned': str(total_earned),
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an active investment and refund the amount."""
        investment = self.get_object()
        
        # Only allow cancelling active investments
        if investment.status != 'active':
            return Response(
                {'detail': 'Only active investments can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Change status to cancelled (signal will handle refund)
        investment.status = 'cancelled'
        investment.save()
        
        return Response({
            'message': 'Investment cancelled successfully. Amount has been refunded.',
            'investment': UserInvestmentSerializer(investment).data
        }, status=status.HTTP_200_OK)


@ensure_csrf_cookie
def investments_page(request):
    """Render investments page with plans and user investments."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Handle investment cancellation
    if request.method == 'POST' and 'cancel_investment' in request.POST:
        investment_id = request.POST.get('investment_id')
        
        try:
            investment = UserInvestment.objects.get(id=investment_id, user=request.user)
            
            if investment.status != 'active':
                context_data = {
                    'plans': InvestmentPlan.objects.filter(is_active=True).order_by('roi_percentage'),
                    'user_investments': UserInvestment.objects.filter(user=request.user).order_by('-created_at'),
                    'balance': request.user.balance,
                    'error': 'Only active investments can be cancelled.'
                }
                return render(request, 'investments.html', context_data)
            
            # Cancel investment (signal will handle refund)
            investment.status = 'cancelled'
            investment.save()
            
            context_data = {
                'plans': InvestmentPlan.objects.filter(is_active=True).order_by('roi_percentage'),
                'user_investments': UserInvestment.objects.filter(user=request.user).order_by('-created_at'),
                'balance': request.user.balance,
                'success': f'Investment cancelled successfully! ${investment.amount} refunded to your balance.'
            }
            return render(request, 'investments.html', context_data)
            
        except UserInvestment.DoesNotExist:
            context_data = {
                'plans': InvestmentPlan.objects.filter(is_active=True).order_by('roi_percentage'),
                'user_investments': UserInvestment.objects.filter(user=request.user).order_by('-created_at'),
                'balance': request.user.balance,
                'error': 'Investment not found.'
            }
            return render(request, 'investments.html', context_data)
    
    # Handle form submission (subscribe to plan)
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        amount = request.POST.get('amount')
        
        context_data = {
            'plans': InvestmentPlan.objects.filter(is_active=True).order_by('roi_percentage'),
            'user_investments': UserInvestment.objects.filter(user=request.user).order_by('-created_at'),
            'balance': request.user.balance,
        }
        
        if not plan_id or not amount:
            context_data['error'] = 'Plan and amount are required.'
            return render(request, 'investments.html', context_data)
        
        try:
            plan = InvestmentPlan.objects.get(id=plan_id, is_active=True)
            amount = Decimal(amount)
            
            if amount < plan.minimum_investment:
                context_data['error'] = f'Minimum investment is ${plan.minimum_investment}.'
                return render(request, 'investments.html', context_data)
            
            if plan.maximum_investment and amount > plan.maximum_investment:
                context_data['error'] = f'Maximum investment is ${plan.maximum_investment}.'
                return render(request, 'investments.html', context_data)
            
            if request.user.balance < amount:
                context_data['error'] = 'Insufficient balance.'
                return render(request, 'investments.html', context_data)
            
            # Create investment
            end_date = timezone.now() + timedelta(days=plan.duration_days)
            investment = UserInvestment.objects.create(
                user=request.user,
                plan=plan,
                amount=amount,
                end_date=end_date,
                status='active'
            )
            
            # Deduct amount from balance
            request.user.balance -= amount
            request.user.total_invested += amount
            request.user.save()
            
            context_data['success'] = f'Investment in {plan.name} created successfully!'
            context_data['user_investments'] = UserInvestment.objects.filter(user=request.user).order_by('-created_at')
            context_data['balance'] = request.user.balance
            
            return render(request, 'investments.html', context_data)
        
        except InvestmentPlan.DoesNotExist:
            context_data['error'] = 'Invalid investment plan.'
            return render(request, 'investments.html', context_data)
        except ValueError:
            context_data['error'] = 'Invalid amount.'
            return render(request, 'investments.html', context_data)
    
    # GET request - show page
    plans = InvestmentPlan.objects.filter(is_active=True).order_by('roi_percentage')
    user_investments = UserInvestment.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'investments.html', {
        'plans': plans,
        'user_investments': user_investments,
        'balance': request.user.balance,
    })
