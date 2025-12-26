"""
Withdrawals views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from decimal import Decimal
from .models import Withdrawal
from .serializers import WithdrawalSerializer, CreateWithdrawalSerializer


class WithdrawalViewSet(viewsets.ModelViewSet):
    """Withdrawal viewset."""
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateWithdrawalSerializer
        return WithdrawalSerializer
    
    def perform_create(self, serializer):
        """Create withdrawal for current user."""
        serializer.save(user=self.request.user, status='pending')
    
    @action(detail=False, methods=['post'])
    def request_withdrawal(self, request):
        """Request a withdrawal."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            
            # Check if user has sufficient balance
            if request.user.balance < amount:
                return Response(
                    {'detail': 'Insufficient balance for withdrawal.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            withdrawal = serializer.save(user=request.user, status='pending')
            return Response({
                'message': 'Withdrawal request submitted successfully.',
                'withdrawal': WithdrawalSerializer(withdrawal).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_withdrawals(self, request):
        """Get all user withdrawals."""
        withdrawals = self.get_queryset()
        serializer = self.get_serializer(withdrawals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_withdrawals(self, request):
        """Get pending withdrawals."""
        withdrawals = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(withdrawals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def withdrawal_history(self, request):
        """Get withdrawal history (completed withdrawals)."""
        withdrawals = self.get_queryset().filter(status='completed')
        total_withdrawn = sum(w.amount for w in withdrawals)
        serializer = self.get_serializer(withdrawals, many=True)
        return Response({
            'withdrawals': serializer.data,
            'total_withdrawn': str(total_withdrawn)
        })


@ensure_csrf_cookie
def withdrawals_page(request):
    """Render withdrawals page with history."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Handle form submission
    if request.method == 'POST':
        amount = request.POST.get('amount')
        cryptocurrency = request.POST.get('cryptocurrency')
        wallet_address = request.POST.get('wallet_address')
        
        if not amount or not cryptocurrency or not wallet_address:
            context = {
                'withdrawals': Withdrawal.objects.filter(user=request.user).order_by('-created_at'),
                'balance': request.user.balance,
                'error': 'All fields are required.',
            }
            return render(request, 'withdrawals.html', context)
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            if request.user.balance < amount:
                context = {
                    'withdrawals': Withdrawal.objects.filter(user=request.user).order_by('-created_at'),
                    'balance': request.user.balance,
                    'error': 'Insufficient balance.',
                }
                return render(request, 'withdrawals.html', context)
            
            # Create withdrawal
            withdrawal = Withdrawal.objects.create(
                user=request.user,
                amount=amount,
                cryptocurrency=cryptocurrency,
                wallet_address=wallet_address,
                status='pending'
            )
            
            # Deduct from balance
            request.user.balance -= amount
            request.user.save()
            
            context = {
                'withdrawals': Withdrawal.objects.filter(user=request.user).order_by('-created_at'),
                'balance': request.user.balance,
                'success': 'Withdrawal request submitted successfully!',
            }
            return render(request, 'withdrawals.html', context)
        except ValueError as e:
            context = {
                'withdrawals': Withdrawal.objects.filter(user=request.user).order_by('-created_at'),
                'balance': request.user.balance,
                'error': str(e),
            }
            return render(request, 'withdrawals.html', context)
    
    # GET request - show page
    user_withdrawals = Withdrawal.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'withdrawals.html', {
        'withdrawals': user_withdrawals,
        'balance': request.user.balance,
    })
