"""
Deposits views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from decimal import Decimal
from .models import Deposit, CryptoWallet
from .serializers import DepositSerializer, CreateDepositSerializer, CryptoWalletSerializer


class CryptoWalletViewSet(viewsets.ReadOnlyModelViewSet):
    """Crypto wallet viewset - read only for users."""
    queryset = CryptoWallet.objects.filter(is_active=True)
    serializer_class = CryptoWalletSerializer
    permission_classes = [AllowAny]


class DepositViewSet(viewsets.ModelViewSet):
    """Deposit viewset."""
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateDepositSerializer
        return DepositSerializer
    
    def perform_create(self, serializer):
        """Create deposit for current user."""
        serializer.save(user=self.request.user, status='pending')
    
    @action(detail=False, methods=['get'])
    def my_deposits(self, request):
        """Get all user deposits."""
        deposits = self.get_queryset()
        serializer = self.get_serializer(deposits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_deposits(self, request):
        """Get pending deposits."""
        deposits = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(deposits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved_deposits(self, request):
        """Get approved deposits."""
        deposits = self.get_queryset().filter(status='approved')
        total = sum(d.amount for d in deposits)
        serializer = self.get_serializer(deposits, many=True)
        return Response({
            'deposits': serializer.data,
            'total_approved': str(total)
        })
    
    @action(detail=False, methods=['post'])
    def submit_deposit(self, request):
        """Submit a new deposit."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if cryptocurrency is active
            try:
                crypto_wallet = CryptoWallet.objects.get(
                    cryptocurrency=serializer.validated_data['cryptocurrency'],
                    is_active=True
                )
            except CryptoWallet.DoesNotExist:
                return Response(
                    {'detail': 'This cryptocurrency is not currently active.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            deposit = serializer.save(user=request.user, status='pending')
            return Response({
                'message': 'Deposit submitted successfully. Awaiting admin approval.',
                'deposit': DepositSerializer(deposit).data,
                'wallet_address': crypto_wallet.wallet_address
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
def deposits_page(request):
    """Render deposits page with wallets and user deposit history."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get wallets and user deposits first (for all cases)
    wallets = CryptoWallet.objects.filter(is_active=True)
    user_deposits = Deposit.objects.filter(user=request.user).order_by('-created_at').distinct()
    
    context_data = {
        'wallets': wallets,
        'deposits': user_deposits,
        'balance': request.user.balance,
    }
    
    # Handle form submission
    if request.method == 'POST':
        cryptocurrency = request.POST.get('cryptocurrency')
        amount = request.POST.get('amount')
        proof_type = request.POST.get('proof_type')
        proof_content = request.POST.get('proof_content')
        
        if not cryptocurrency or not amount or not proof_type or not proof_content:
            context_data['error'] = 'All fields are required.'
            return render(request, 'deposits.html', context_data)
        
        try:
            # Check cryptocurrency is active
            wallet = CryptoWallet.objects.get(cryptocurrency=cryptocurrency, is_active=True)
            amount = Decimal(amount)
            
            if amount <= 0:
                raise ValueError('Amount must be greater than 0.')
            
            # Create deposit
            deposit = Deposit.objects.create(
                user=request.user,
                cryptocurrency=cryptocurrency,
                amount=amount,
                proof_type=proof_type,
                proof_content=proof_content,
                status='pending'
            )
            
            context_data['success'] = 'Deposit submitted successfully! Admin will review and approve it.'
            # Refresh deposits list from database
            context_data['deposits'] = Deposit.objects.filter(user=request.user).order_by('-created_at').distinct()
            
            return render(request, 'deposits.html', context_data)
        
        except CryptoWallet.DoesNotExist:
            context_data['error'] = 'This cryptocurrency is not active.'
            return render(request, 'deposits.html', context_data)
        except ValueError as e:
            context_data['error'] = str(e)
            return render(request, 'deposits.html', context_data)
    
    # GET request - return with current context
    return render(request, 'deposits.html', context_data)
