from django.db import models

class Student(models.Model):
    name        = models.CharField(max_length=200)
    email       = models.EmailField()
    mobile      = models.CharField(max_length=20, blank=True, null=True)
    course_name = models.CharField(max_length=200)
    link        = models.URLField()
    email_sent  = models.BooleanField(default=False)
    sms_sent    = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.course_name}"