from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'name']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='last Name', max_length=30)

    EMAIL_VALIDATION = '^([a-zA-Z]|-)+.(\d)+@(osu|buckeyemail.osu).edu$'

    email = forms.EmailField(label='Email Address', required=True, 
                             help_text='name.#@osu.edu Ex: buckeye.1@osu.edu', 
                             validators=[RegexValidator(EMAIL_VALIDATION, "Email must be of the form [name].#@osu.edu")])
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')