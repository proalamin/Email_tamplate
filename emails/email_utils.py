"""
Email utility functions for handling multiple accounts and rate limiting
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import time


def get_available_email_account():
    """
    Get an available email account from database that hasn't reached its daily limit
    Priority-based selection: Lower priority number = Higher priority
    Returns: EmailAccount object or None if all accounts are at limit
    """
    from .models import EmailAccount
    
    # Order by priority first (0 = highest), then by usage
    accounts = EmailAccount.objects.filter(is_active=True).order_by('priority', 'sent_today')
    
    for account in accounts:
        account.reset_if_new_day()
        if account.can_send():
            return account
    
    return None


def send_email_with_rotation(subject, text_message, html_message, recipient_email):
    """
    Send email using account rotation from database
    
    Args:
        subject: Email subject
        text_message: Plain text message
        html_message: HTML message
        recipient_email: Recipient's email address
    
    Returns:
        dict: {'success': bool, 'message': str, 'account_used': str}
    """
    account = get_available_email_account()
    
    if not account:
        return {
            'success': False,
            'message': 'All email accounts have reached their daily limit. Please add more accounts or try again tomorrow.',
            'account_used': None
        }
    
    try:
        # Create email with the selected account
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=account.email,
            to=[recipient_email]
        )
        email.attach_alternative(html_message, "text/html")
        
        # Configure SMTP connection with account credentials
        email.connection = None  # Use default connection but with custom credentials
        
        # Send email
        from django.core.mail import get_connection
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=account.email,
            password=account.password,
            use_tls=settings.EMAIL_USE_TLS,
        )
        
        email.connection = connection
        email.send(fail_silently=False)
        
        # Update usage counter
        account.increment_sent()
        
        # Add delay to avoid rate limiting
        time.sleep(getattr(settings, 'EMAIL_SEND_DELAY', 1))
        
        return {
            'success': True,
            'message': 'Email sent successfully',
            'account_used': account.email,
            'sent_today': account.sent_today,
            'remaining': account.daily_limit - account.sent_today
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send email: {str(e)}',
            'account_used': account.email
        }


def get_email_stats():
    """
    Get statistics about email usage from database
    
    Returns:
        dict: Statistics about each account's usage
    """
    from .models import EmailAccount
    
    accounts = EmailAccount.objects.filter(is_active=True)
    
    stats = []
    total_sent = 0
    total_remaining = 0
    
    for account in accounts:
        account.reset_if_new_day()
        
        remaining = account.daily_limit - account.sent_today
        total_sent += account.sent_today
        total_remaining += remaining
        
        stats.append({
            'id': account.id,
            'email': account.email,
            'sent_today': account.sent_today,
            'daily_limit': account.daily_limit,
            'remaining': remaining,
            'percentage_used': round((account.sent_today / account.daily_limit) * 100, 2) if account.daily_limit > 0 else 0,
            'last_reset_date': str(account.last_reset_date)
        })
    
    return {
        'accounts': stats,
        'total_sent_today': total_sent,
        'total_remaining': total_remaining,
        'total_capacity': sum(acc.daily_limit for acc in accounts),
        'total_accounts': accounts.count()
    }
