"""
Email utilities for user notifications.
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_admin_dashboard_url():
    """Get admin dashboard URL."""
    if settings.DEBUG:
        return "http://127.0.0.1:8001/admin/"
    else:
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'yourdomain.com'
        return f"https://{domain}/admin/"


def get_dashboard_url():
    """Get user dashboard URL."""
    if settings.DEBUG:
        return "http://127.0.0.1:8001/dashboard/"
    else:
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'yourdomain.com'
        return f"https://{domain}/dashboard/"


def send_password_reset_email(user, reset_link):
    """Send password reset email to user."""
    subject = 'Reset Your Password - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fff; margin-bottom: 20px;">Password Reset Request</h2>
            <p style="color: #ccc; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #ccc; line-height: 1.6;">
                We received a request to reset your password for your Tesla Investment Platform account.
            </p>
            <p style="color: #ccc; line-height: 1.6;">
                Click the button below to reset your password:
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #fff; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p style="color: #999; font-size: 12px; line-height: 1.6;">
                If you didn't request this, you can safely ignore this email.
                This link will expire in 24 hours.
            </p>
            <p style="color: #999; font-size: 12px; line-height: 1.6;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <span style="color: #666;">{reset_link}</span>
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_deposit_notification(deposit):
    """Send email notification when deposit is approved."""
    user = deposit.user
    subject = f'Deposit {"Approved" if deposit.status == "approved" else "Rejected"} - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fff; margin-bottom: 20px;">Deposit {deposit.get_status_display()}</h2>
            <p style="color: #ccc; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #ccc; line-height: 1.6;">
                Your deposit of <strong style="color: #fff;">${deposit.amount}</strong> has been <strong>{deposit.get_status_display().lower()}</strong>.
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">Amount: <strong style="color: #fff;">${deposit.amount}</strong></p>
                <p style="color: #999; margin: 5px 0;">Method: <strong style="color: #fff;">{deposit.get_payment_method_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Status: <strong style="color: {'#4ade80' if deposit.status == 'approved' else '#f87171'};">{deposit.get_status_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Date: <strong style="color: #fff;">{deposit.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            {"<p style='color: #4ade80; line-height: 1.6;'>✓ Your account balance has been credited.</p>" if deposit.status == 'approved' else "<p style='color: #f87171; line-height: 1.6;'>✗ Please contact support if you have questions.</p>"}
            <div style="text-align: center; margin: 30px 0;">
                <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'http://127.0.0.1:8001'}/dashboard/" style="background-color: #fff; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_withdrawal_notification(withdrawal):
    """Send email notification when withdrawal is processed."""
    user = withdrawal.user
    subject = f'Withdrawal {withdrawal.get_status_display()} - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fff; margin-bottom: 20px;">Withdrawal {withdrawal.get_status_display()}</h2>
            <p style="color: #ccc; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #ccc; line-height: 1.6;">
                Your withdrawal request of <strong style="color: #fff;">${withdrawal.amount}</strong> has been <strong>{withdrawal.get_status_display().lower()}</strong>.
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">Amount: <strong style="color: #fff;">${withdrawal.amount}</strong></p>
                <p style="color: #999; margin: 5px 0;">Method: <strong style="color: #fff;">{withdrawal.get_withdrawal_method_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Status: <strong style="color: {'#4ade80' if withdrawal.status == 'completed' else '#f87171' if withdrawal.status == 'rejected' else '#fbbf24'};">{withdrawal.get_status_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Date: <strong style="color: #fff;">{withdrawal.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            {"<p style='color: #4ade80; line-height: 1.6;'>✓ Your funds have been sent to your account.</p>" if withdrawal.status == 'completed' else "<p style='color: #f87171; line-height: 1.6;'>✗ Your balance has been refunded. Contact support for details.</p>" if withdrawal.status == 'rejected' else "<p style='color: #fbbf24; line-height: 1.6;'>⏳ Your withdrawal is being processed.</p>"}
            <div style="text-align: center; margin: 30px 0;">
                <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'http://127.0.0.1:8001'}/withdrawals/" style="background-color: #fff; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Withdrawals
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_admin_deposit_notification(deposit):
    """Send email notification to admin when new deposit is created."""
    if not settings.ADMIN_EMAIL:
        return
    
    user = deposit.user
    subject = f'New Deposit Request - ${deposit.amount} from {user.get_full_name()}'
    admin_url = get_admin_dashboard_url()
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fbbf24; margin-bottom: 20px;">⚠️ New Deposit Pending Approval</h2>
            <p style="color: #ccc; line-height: 1.6;">
                A new deposit request requires your attention.
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">User: <strong style="color: #fff;">{user.get_full_name()} ({user.email})</strong></p>
                <p style="color: #999; margin: 5px 0;">Amount: <strong style="color: #4ade80;">${deposit.amount}</strong></p>
                <p style="color: #999; margin: 5px 0;">Method: <strong style="color: #fff;">{deposit.get_payment_method_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Status: <strong style="color: #fbbf24;">Pending</strong></p>
                <p style="color: #999; margin: 5px 0;">Date: <strong style="color: #fff;">{deposit.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
                {"<p style='color: #999; margin: 5px 0;'>Transaction ID: <strong style='color: #fff;'>" + str(deposit.transaction_id) + "</strong></p>" if deposit.transaction_id else ""}
            </div>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{admin_url}deposits/deposit/{deposit.pk}/change/" style="background-color: #fbbf24; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Review Deposit
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )


def send_admin_withdrawal_notification(withdrawal):
    """Send email notification to admin when new withdrawal is created."""
    if not settings.ADMIN_EMAIL:
        return
    
    user = withdrawal.user
    subject = f'New Withdrawal Request - ${withdrawal.amount} from {user.get_full_name()}'
    admin_url = get_admin_dashboard_url()
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fbbf24; margin-bottom: 20px;">⚠️ New Withdrawal Pending Approval</h2>
            <p style="color: #ccc; line-height: 1.6;">
                A new withdrawal request requires your attention.
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">User: <strong style="color: #fff;">{user.get_full_name()} ({user.email})</strong></p>
                <p style="color: #999; margin: 5px 0;">Amount: <strong style="color: #f87171;">${withdrawal.amount}</strong></p>
                <p style="color: #999; margin: 5px 0;">Method: <strong style="color: #fff;">{withdrawal.get_withdrawal_method_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">User Balance: <strong style="color: #4ade80;">${user.balance}</strong></p>
                <p style="color: #999; margin: 5px 0;">Status: <strong style="color: #fbbf24;">Pending</strong></p>
                <p style="color: #999; margin: 5px 0;">Date: <strong style="color: #fff;">{withdrawal.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
                {"<p style='color: #999; margin: 5px 0;'>Wallet Address: <strong style='color: #fff;'>" + str(withdrawal.wallet_address) + "</strong></p>" if withdrawal.wallet_address else ""}
            </div>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{admin_url}withdrawals/withdrawal/{withdrawal.pk}/change/" style="background-color: #fbbf24; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Review Withdrawal
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )


def send_admin_support_notification(ticket):
    """Send email notification to admin when new support ticket is created."""
    if not settings.ADMIN_EMAIL:
        return
    
    user = ticket.user
    subject = f'New Support Ticket #{ticket.pk} - {ticket.subject}'
    admin_url = get_admin_dashboard_url()
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fbbf24; margin-bottom: 20px;">📩 New Support Ticket</h2>
            <p style="color: #ccc; line-height: 1.6;">
                A new support ticket has been created and needs your response.
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">Ticket: <strong style="color: #fff;">#{ticket.pk}</strong></p>
                <p style="color: #999; margin: 5px 0;">User: <strong style="color: #fff;">{user.get_full_name()} ({user.email})</strong></p>
                <p style="color: #999; margin: 5px 0;">Subject: <strong style="color: #fff;">{ticket.subject}</strong></p>
                <p style="color: #999; margin: 5px 0;">Category: <strong style="color: #fff;">{ticket.get_category_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Priority: <strong style="color: {'#f87171' if ticket.priority == 'high' else '#fbbf24' if ticket.priority == 'medium' else '#4ade80'};">{ticket.get_priority_display()}</strong></p>
                <p style="color: #999; margin: 5px 0;">Date: <strong style="color: #fff;">{ticket.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            <div style="background-color: #111; padding: 15px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 0; font-size: 14px;">Message:</p>
                <p style="color: #ccc; margin: 10px 0; line-height: 1.6;">{ticket.message[:200]}{"..." if len(ticket.message) > 200 else ""}</p>
            </div>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{admin_url}support/supportticket/{ticket.pk}/change/" style="background-color: #fbbf24; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Reply to Ticket
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )
