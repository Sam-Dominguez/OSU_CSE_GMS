import logging
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from .services import permissions

LOGGER = logging.getLogger('django')

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Using IntegerField instead of BooleanField b/c SQLLite does not support boolean values: (1 = True, 0 = False)
    in_columbus = models.IntegerField(null=True)
    previous_grader = models.IntegerField(null=True)

    # Either null or a course number (Ex: 2221)
    graded_last_term = models.CharField(max_length=4, blank=True)

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # tie Django 'User' to OSU CSE 'user'
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.last_name + ', ' + self.first_name
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return 'No name available'

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

    instructor = models.ForeignKey(Instructor, on_delete=models.SET_DEFAULT, default=None, null=True)
    
    INSTRUCTION_MODES = [
        ('SYNCHRONOUS', 'SYNCHRONOUS'),
        ('ASYNCHRONOUS', 'ASYNCHRONOUS')
    ]
    instruction_mode = models.CharField(max_length=13, choices=INSTRUCTION_MODES)
    
    time = models.CharField(max_length=30, blank=True)
    days_of_week = models.CharField(max_length=30, blank=True)
    classroom = models.CharField(max_length=30, blank=True)

    num_graders_needed = models.IntegerField(default=1)

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


# Assign the user that is tied to a model to a group on save
'''
Raw flag is true if the data is coming from a fixture, we do not want to modify fixture data here
so it remains consistent with the json file data (Also not all db tables may be instantiated at the time of editing)
'''
@receiver(models.signals.post_save, sender=Student)
def assign_student_group(sender, instance, created, *args, **kwargs):
    # Order is important in the if statement, using short circuit evaluation
    if not kwargs.get('raw', False) and instance.user:
        student_group = Group.objects.get_or_create(name=permissions.STUDENT_GROUP)
        instance.user.groups.add(student_group[0])
        LOGGER.info(f'User {instance.user.username} added to student group')

@receiver(models.signals.post_save, sender=Administrator)
def assign_administrator_group(sender, instance, created, *args, **kwargs):
    if not kwargs.get('raw', False) and instance.user:
        administrator_group = Group.objects.get_or_create(name=permissions.ADMINISTRATOR_GROUP)
        instance.user.groups.add(administrator_group[0])
        LOGGER.info(f'User {instance.user.username} added to administrator group')

@receiver(models.signals.post_save, sender=Instructor)
def assign_instructor_group(sender, instance, created, *args, **kwargs):
    if not kwargs.get('raw', False) and instance.user:
        instructor_group = Group.objects.get_or_create(name=permissions.INSTRUCTOR_GROUP)
        instance.user.groups.add(instructor_group[0])
        LOGGER.info(f'User {instance.user.username} added to instructor group')