"""
Support ticket signals.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SupportTicket


@receiver(post_save, sender=SupportTicket)
def send_support_ticket_email(sender, instance, created, **kwargs):
    """Send email notification to admin when new support ticket is created."""
    if created:
        try:
            from apps.users.emails import send_admin_support_notification
            send_admin_support_notification(instance)
        except Exception as e:
            print(f"Failed to send support ticket email: {e}")
