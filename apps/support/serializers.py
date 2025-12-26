"""
Support serializers.
"""

from rest_framework import serializers
from .models import SupportTicket, SupportReply


class SupportReplySerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    
    class Meta:
        model = SupportReply
        fields = [
            'id', 'sender', 'sender_name', 'sender_email',
            'message', 'is_from_admin', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    replies = SupportReplySerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'user_name', 'subject', 'message',
            'priority', 'status', 'attachment', 'created_at',
            'updated_at', 'resolved_at', 'replies'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at', 'resolved_at', 'replies'
        ]


class CreateSupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message', 'priority', 'attachment']


class AddSupportReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportReply
        fields = ['message']
