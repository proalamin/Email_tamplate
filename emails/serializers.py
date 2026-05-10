from rest_framework import serializers
from .models import Student, EmailTemplate, EmailAccount

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = '__all__'


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'


class EmailAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAccount
        fields = ['id', 'email', 'daily_limit', 'sent_today', 'last_reset_date', 'is_active', 'priority', 'created_at']
        # Don't expose password in serializer