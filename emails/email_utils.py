"""
Email utility functions for handling multiple accounts and rate limiting
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
import time

# Track email usage per account
email_usage = {}


def reset_daily_counters():
    """Reset counters if it's a new day"""
    global email_usage
    today = datetime.now().date()
    
    for account in settings.EMAIL_ACCOUNTS:
        email = account['email']
        if email not in email_usage:
            email_usage[email] = {'count': 0, 'date': today}
        elif email_usage[email]['date'] != today:
            email_usage[email] = {'count': 0, 'date': today}


def get_available_email_account():
    """
    Get an available email account that hasn't reached its daily limit
    Returns: dict with email and password, or None if all accounts are at limit
    """
    reset_daily_counters()
    
    for account in settings.EMAIL_ACCOUNTS:
        email = account['email']
        daily_limit = account['daily_limit']
        
        if email not in email_usage:
            email_usage[email] = {'count': 0, 'date': datetime.now().date()}
        
        if email_usage[email]['count'] < daily_limit:
            return account
    
    return None


def send_email_with_rotation(subject, text_message, html_message, recipient_email):
    """
    Send email using account rotation
    
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
            'message': 'All email accounts have reached their daily limit. Please try again tomorrow.',
            'account_used': None
        }
    
    try:
        # Create email with the selected account
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=account['email'],
            to=[recipient_email]
        )
        email.attach_alternative(html_message, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        # Update usage counter
        email_usage[account['email']]['count'] += 1
        
        # Add delay to avoid rate limiting
        time.sleep(settings.EMAIL_SEND_DELAY)
        
        return {
            'success': True,
            'message': 'Email sent successfully',
            'account_used': account['email']
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to send email: {str(e)}',
            'account_used': account['email']
        }


def get_email_stats():
    """
    Get statistics about email usage
    
    Returns:
        dict: Statistics about each account's usage
    """
    reset_daily_counters()
    
    stats = []
    total_sent = 0
    total_remaining = 0
    
    for account in settings.EMAIL_ACCOUNTS:
        email = account['email']
        daily_limit = account['daily_limit']
        
        if email in email_usage:
            sent = email_usage[email]['count']
        else:
            sent = 0
        
        remaining = daily_limit - sent
        total_sent += sent
        total_remaining += remaining
        
        stats.append({
            'email': email,
            'sent_today': sent,
            'daily_limit': daily_limit,
            'remaining': remaining,
            'percentage_used': round((sent / daily_limit) * 100, 2) if daily_limit > 0 else 0
        })
    
    return {
        'accounts': stats,
        'total_sent_today': total_sent,
        'total_remaining': total_remaining,
        'total_capacity': sum(acc['daily_limit'] for acc in settings.EMAIL_ACCOUNTS)
    }
