from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Using IntegerField instead of BooleanField b/c SQLLite does not support boolean values: (1 = True, 0 = False)
    in_columbus = models.IntegerField()
    previous_grader = models.IntegerField()

    # Either None or a course number (Ex: 2221)
    graded_last_term = models.CharField(max_length=4, default=None)

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
    name = models.CharField(max_length=200)

    def __str__(self):
        return 'CSE ' + self.course_number + ': ' + self.name

class Section(models.Model):
    course_number = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=30)
    # term (AU, SU, SP) + year (XXXX)
    semester = models.CharField(max_length=6)

    instructor = models.ForeignKey(Instructor, on_delete=models.SET_DEFAULT, default='No Instructor')
    
    INSTRUCTION_MODES = [
        ('SYNCHRNONOUS', 'SYNCHRNONOUS'),
        ('ASYNCHRNONOUS', 'ASYNCHRNONOUS')
    ]
    instruction_mode = models.CharField(max_length=13, choices=INSTRUCTION_MODES)
    
    time = models.CharField(max_length=30, blank=True)
    days_of_week = models.CharField(max_length=30, blank=True)
    classroom = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = [['course_number', 'section_number', 'semester']]

class Assignment(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    section_number = models.ForeignKey(Section, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined')
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    class Meta:
        unique_together = [['student_id', 'section_number']]

class UnassignedStudent(models.Model):
    student_id = models.OneToOneField(Student, primary_key=True, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)

class PreviousClassTaken(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_number = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.CharField(max_length=40, blank=True)
    pref_num = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(3)])

    class Meta:
        unique_together = [['student_id', 'course_number']]
