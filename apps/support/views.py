"""
Support views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SupportTicket, SupportReply
from .serializers import (
    SupportTicketSerializer, CreateSupportTicketSerializer,
    AddSupportReplySerializer, SupportReplySerializer
)


class SupportTicketViewSet(viewsets.ModelViewSet):
    """Support ticket viewset."""
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateSupportTicketSerializer
        return SupportTicketSerializer
    
    def perform_create(self, serializer):
        """Create ticket for current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        """Get all user support tickets."""
        tickets = self.get_queryset()
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def open_tickets(self, request):
        """Get open tickets."""
        tickets = self.get_queryset().filter(status='open')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_reply(self, request, pk=None):
        """Add a reply to a support ticket."""
        ticket = self.get_object()
        serializer = AddSupportReplySerializer(data=request.data)
        
        if serializer.is_valid():
            reply = SupportReply.objects.create(
                ticket=ticket,
                sender=request.user,
                message=serializer.validated_data['message'],
                is_from_admin=False
            )
            
            # Update ticket status to in_progress if user replies
            if ticket.status == 'open':
                ticket.status = 'in_progress'
                ticket.save()
            
            return Response({
                'message': 'Reply added successfully',
                'reply': SupportReplySerializer(reply).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def ticket_detail(self, request, pk=None):
        """Get ticket detail with all replies."""
        ticket = self.get_object()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_ticket(self, request):
        """Create a new support ticket."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save(user=request.user)
            return Response({
                'message': 'Support ticket created successfully',
                'ticket': SupportTicketSerializer(ticket).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
