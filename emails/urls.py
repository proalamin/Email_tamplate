from django.urls import path
from .views import (
    home,
    UploadStudentsView, 
    StudentListView, 
    SendEmailsView,
    SendCustomTemplateView,
    DeleteStudentView,
    DeleteAllStudentsView,
    AddStudentView,
    UpdateStudentView,
    EmailStatsView,
    EmailAccountListView,
    AddEmailAccountView,
    UpdateEmailAccountView,
    DeleteEmailAccountView,
    SetAccountPriorityView,
    MoveAccountUpView,
    MoveAccountDownView
)

urlpatterns = [
    path('', home, name='home'),
    path('upload/', UploadStudentsView.as_view()),
    path('students/', StudentListView.as_view()),
    path('send-emails/', SendEmailsView.as_view()),
    path('send-template/', SendCustomTemplateView.as_view()),
    path('add-student/', AddStudentView.as_view()),
    path('update-student/', UpdateStudentView.as_view()),
    path('delete-student/<int:student_id>/', DeleteStudentView.as_view()),
    path('delete-all/', DeleteAllStudentsView.as_view()),
    path('email-stats/', EmailStatsView.as_view()),
    # Email Account Management
    path('email-accounts/', EmailAccountListView.as_view()),
    path('add-email-account/', AddEmailAccountView.as_view()),
    path('update-email-account/<int:account_id>/', UpdateEmailAccountView.as_view()),
    path('delete-email-account/<int:account_id>/', DeleteEmailAccountView.as_view()),
    path('set-account-priority/<int:account_id>/', SetAccountPriorityView.as_view()),
    path('move-account-up/<int:account_id>/', MoveAccountUpView.as_view()),
    path('move-account-down/<int:account_id>/', MoveAccountDownView.as_view()),
]