from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import pandas as pd
import time

from .models import Student
from .serializers import StudentSerializer

# Rate limiting: 20 emails per hour
EMAILS_PER_HOUR = 20
EMAIL_DELAY_SECONDS = 3600 / EMAILS_PER_HOUR  # 180 seconds = 3 minutes between emails


def home(request):
    """Home page with UI"""
    return render(request, 'index.html')


def send_course_email(student):
    """Helper function to send course enrollment email"""
    subject = f"You're Interested in {student.course_name} – Enroll Now!"
    
    text_message = f"""Dear {student.name},

You are interested in {student.course_name}.

Please click the link below to enroll:
{student.link}

Best regards,
Innovative Skills BD"""

    html_message = render_to_string('emails/course_enrollment.html', {
        'name': student.name,
        'course_name': student.course_name,
        'link': student.link,
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[student.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)


class UploadStudentsView(APIView):
    """Upload Excel file - emails will be sent gradually (20 per hour)"""
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({'error': f'Failed to read Excel file: {str(e)}'}, status=400)

        required_columns = ['Name', 'Email', 'Course Name', 'Link']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response({'error': f'Missing columns: {", ".join(missing_columns)}'}, status=400)

        imported = 0
        emails_sent = 0
        failed_emails = []
        skipped_rows = 0
        email_count_this_batch = 0

        for index, row in df.iterrows():
            try:
                # Check if all required fields are present and not empty
                if pd.isna(row['Name']) or pd.isna(row['Email']) or pd.isna(row['Course Name']) or pd.isna(row['Link']):
                    skipped_rows += 1
                    continue
                
                # Check if fields are not empty strings
                if not str(row['Name']).strip() or not str(row['Email']).strip() or not str(row['Course Name']).strip() or not str(row['Link']).strip():
                    skipped_rows += 1
                    continue
                
                student, created = Student.objects.get_or_create(
                    email=row['Email'],
                    defaults={
                        'name': row['Name'],
                        'course_name': row['Course Name'],
                        'link': row['Link'],
                    }
                )
                
                if created:
                    imported += 1
                
                # Send email with rate limiting (20 per hour)
                if not student.email_sent and email_count_this_batch < EMAILS_PER_HOUR:
                    try:
                        send_course_email(student)
                        student.email_sent = True
                        student.save()
                        emails_sent += 1
                        email_count_this_batch += 1
                        
                        # Add delay between emails (3 minutes)
                        if email_count_this_batch < EMAILS_PER_HOUR:
                            time.sleep(EMAIL_DELAY_SECONDS)
                    except Exception as email_error:
                        failed_emails.append(f"{student.email}: {str(email_error)}")
                        
            except Exception as e:
                return Response({'error': f'Error processing row: {str(e)}'}, status=400)

        pending_count = Student.objects.filter(email_sent=False).count()
        
        response_data = {
            'message': f'{imported} new students imported, {emails_sent} emails sent!',
            'pending': pending_count,
            'info': f'Rate limit: 20 emails/hour. {pending_count} emails pending.'
        }
        
        if skipped_rows > 0:
            response_data['warning'] = f'{skipped_rows} incomplete rows skipped'
            
        if failed_emails:
            response_data['failed_emails'] = failed_emails
            
        return Response(response_data)


class StudentListView(APIView):
    """Get all students"""
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class SendEmailsView(APIView):
    """Send emails to pending students (20 per hour rate limit)"""
    
    def post(self, request):
        students = Student.objects.filter(email_sent=False)[:EMAILS_PER_HOUR]
        
        if not students.exists():
            return Response({'message': 'No pending emails to send'})
        
        sent = 0
        failed_emails = []

        for student in students:
            try:
                send_course_email(student)
                student.email_sent = True
                student.save()
                sent += 1
                
                # Add delay between emails (3 minutes)
                if sent < len(students):
                    time.sleep(EMAIL_DELAY_SECONDS)
            except Exception as e:
                failed_emails.append(f"{student.email}: {str(e)}")

        pending_count = Student.objects.filter(email_sent=False).count()
        
        response_data = {
            'message': f'{sent} emails sent successfully!',
            'pending': pending_count,
            'info': f'{pending_count} emails still pending. Will send 20 per hour.'
        }
        if failed_emails:
            response_data['failed_emails'] = failed_emails
            
        return Response(response_data)



class SendSingleEmailView(APIView):
    """Send email to a single student"""
    
    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            
            if student.email_sent:
                return Response({'error': 'Email already sent to this student'}, status=400)
            
            try:
                send_course_email(student)
                student.email_sent = True
                student.save()
                return Response({'message': f'Email sent successfully to {student.email}'})
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=500)
                
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)



class NotifyAdminView(APIView):
    """Send notification to admin when someone clicks a course link"""
    
    def post(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            
            # Send notification to admin
            subject = f"🔔 Course Link Clicked - {student.name}"
            
            text_message = f"""Admin Notification:

Student {student.name} ({student.email}) clicked on the course link.

Course: {student.course_name}
Link: {student.link}

This is an automated notification from Email Automation System.
"""

            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
        .content {{ color: #333; line-height: 1.6; }}
        .info-box {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; }}
        .link-btn {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔔 Course Link Clicked</h2>
        </div>
        <div class="content">
            <p><strong>Student Details:</strong></p>
            <div class="info-box">
                <p><strong>Name:</strong> {student.name}</p>
                <p><strong>Email:</strong> {student.email}</p>
                <p><strong>Course:</strong> {student.course_name}</p>
            </div>
            <p>The student clicked on the course enrollment link.</p>
            <a href="{student.link}" class="link-btn">View Course Page</a>
            <p style="margin-top: 20px; color: #999; font-size: 12px;">
                This is an automated notification from Email Automation System.
            </p>
        </div>
    </div>
</body>
</html>
"""

            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.EMAIL_HOST_USER]  # Send to admin (yourself)
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                
                return Response({'message': 'Notification sent to admin', 'link': student.link})
            except Exception as e:
                return Response({'error': f'Failed to send notification: {str(e)}'}, status=500)
                
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)



class DeleteStudentView(APIView):
    """Delete a single student"""
    
    def delete(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            student_name = student.name
            student.delete()
            return Response({'message': f'Student {student_name} deleted successfully'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)


class DeleteAllStudentsView(APIView):
    """Delete all students"""
    
    def delete(self, request):
        count = Student.objects.count()
        Student.objects.all().delete()
        return Response({'message': f'All {count} students deleted successfully'})
