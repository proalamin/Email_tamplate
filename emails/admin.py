from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course_name', 'email_sent')
    list_filter = ('email_sent', 'course_name')
    search_fields = ('name', 'email', 'course_name')
    readonly_fields = ('email_sent',)
