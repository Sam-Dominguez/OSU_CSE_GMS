from django import forms
from django.contrib.auth.models import User
from .models import Student, Administrator, Instructor, Course, Section

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'name']