from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Using IntegerField instead of BooleanField b/c SQLLite does not support boolean values: (1 = True, 0 = False)
    in_columbus = models.IntegerField()
    previous_grader = models.IntegerField()

    previous_classes = models.TextField(blank=True)

class Administrator(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Course(models.Model):
    course_number = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=30)

class Section(models.Model):
    course_number = models.ForeignKey("Course", on_delete=models.CASCADE)
    section_number = models.CharField(max_length=30)
    instructor = models.ForeignKey("Instructor", on_delete=models.SET_DEFAULT, default='No Instructor')
    
    INSTRUCTION_MODES = [
        ('SYNCHRNONOUS', 'SYNCHRNONOUS'),
        ('ASYNCHRNONOUS', 'ASYNCHRNONOUS')
    ]
    instruction_mode = models.CharField(max_length=13, choices=INSTRUCTION_MODES)
    
    # term (AU, SU, SP) + year (XXXX)
    semester = models.CharField(max_length=6)

    time = models.CharField(max_length=30, blank=True)
    days_of_week = models.CharField(max_length=30, blank=True)
    classroom = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = [['course_number', 'section_number']]

