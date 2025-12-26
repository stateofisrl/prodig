"""
Support admin configuration.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from .models import SupportTicket, SupportReply


class SupportReplyFormSet(BaseInlineFormSet):
    """Custom formset to handle sender assignment."""
    
    def save_new(self, form, commit=True):
        """Override to set sender before saving new instances."""
        instance = super().save_new(form, commit=False)
        # Always set sender from request if not already set
        if not instance.sender_id and hasattr(self.__class__, 'request'):
            request = self.__class__.request
            if hasattr(request, 'user') and request.user.is_authenticated:
                instance.sender = request.user
                instance.is_from_admin = True
        if commit:
            instance.save()
        return instance


class SupportReplyInline(admin.TabularInline):
    model = SupportReply
    extra = 1
    fields = ['message', 'is_from_admin']
    formset = SupportReplyFormSet
    
    def get_readonly_fields(self, request, obj=None):
        """Make sender and created_at readonly for existing replies."""
        if obj:  # Editing existing ticket
            return ['sender', 'created_at']
        return []
    
    def get_fields(self, request, obj=None):
        """Show sender and created_at as readonly for existing replies."""
        if obj:  # Editing existing ticket
            return ['sender', 'message', 'is_from_admin', 'created_at']
        else:  # Creating new reply
            return ['message', 'is_from_admin']
    
    def get_formset(self, request, obj=None, **kwargs):
        """Pass request to the formset."""
        FormSet = super().get_formset(request, obj, **kwargs)
        FormSet.request = request
        return FormSet


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'subject', 'priority_badge', 'status_badge', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['user__email', 'subject', 'message']
    readonly_fields = ['user', 'created_at', 'updated_at']
    inlines = [SupportReplyInline]
    actions = ['mark_as_resolved', 'mark_as_closed']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Ticket Info', {
            'fields': ('user', 'subject', 'message', 'attachment')
        }),
        ('Status', {
            'fields': ('priority', 'status', 'resolved_at')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def ticket_id(self, obj):
        return f"#{obj.id}"
    ticket_id.short_description = "Ticket ID"
    
    def priority_badge(self, obj):
        colors = {
            'low': '#28a745',
            'medium': '#ffc107',
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.get_priority_display()
        )
    priority_badge.short_description = "Priority"
    
    def status_badge(self, obj):
        colors = {
            'open': '#dc3545',
            'in_progress': '#ffc107',
            'resolved': '#28a745',
            'closed': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        count = queryset.filter(status__in=['open', 'in_progress']).update(
            status='resolved',
            resolved_at=timezone.now()
        )
        self.message_user(request, f'{count} ticket(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark as resolved'
    
    def mark_as_closed(self, request, queryset):
        count = queryset.filter(status__in=['open', 'in_progress', 'resolved']).update(status='closed')
        self.message_user(request, f'{count} ticket(s) marked as closed.')
    mark_as_closed.short_description = 'Mark as closed'


@admin.register(SupportReply)
class SupportReplyAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'is_from_admin', 'created_at']
    list_filter = ['is_from_admin', 'created_at']
    search_fields = ['ticket__subject', 'sender__email', 'message']
    readonly_fields = ['ticket', 'sender', 'created_at']
    ordering = ['-created_at']
