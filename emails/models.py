from django.db import models
from django.utils import timezone

class Student(models.Model):
    name        = models.CharField(max_length=200)
    email       = models.EmailField()
    mobile      = models.CharField(max_length=20, blank=True, null=True)
    course_name = models.CharField(max_length=200)
    link        = models.URLField()
    email_sent  = models.BooleanField(default=False)
    sms_sent    = models.BooleanField(default=False)
    template_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.course_name}"


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=500)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.subject} - {self.sent_count} sent"


class EmailAccount(models.Model):
    """Store user's email account configurations"""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)  # App password
    daily_limit = models.IntegerField(default=450)
    sent_today = models.IntegerField(default=0)
    last_reset_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  # Lower number = higher priority
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'sent_today']  # Order by priority first, then usage

    def __str__(self):
        return f"{self.email} - Priority {self.priority} - {self.sent_today}/{self.daily_limit}"

    def reset_if_new_day(self):
        """Reset counter if it's a new day"""
        today = timezone.now().date()
        if self.last_reset_date < today:
            self.sent_today = 0
            self.last_reset_date = today
            self.save()

    def can_send(self):
        """Check if account can send more emails"""
        self.reset_if_new_day()
        return self.is_active and self.sent_today < self.daily_limit

    def increment_sent(self):
        """Increment sent counter"""
        self.sent_today += 1
        self.save()