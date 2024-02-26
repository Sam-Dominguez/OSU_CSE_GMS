from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from .models import Student, Course

class GraderForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name','previous_classes']
    
class ClassPrefForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'name']
        widgets = {
            'course_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }