from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Course, Section, Instructor

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'name']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['course_number', 'section_number', 'semester', 'instructor', 'instruction_mode', 'time', 'days_of_week', 'classroom', 'num_graders_needed']
    
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Instructor.objects.all()
        self.fields['instructor'].required = False

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='last Name', max_length=30)

    EMAIL_VALIDATION = '^([a-zA-Z]+-?[a-zA-Z]*)\.(\d)+@(osu|buckeyemail\.osu)\.edu$'

    email = forms.EmailField(label='Email Address', required=True, 
        help_text='name.#@buckeyemail.osu.edu Ex: buckeye.1@buckeyemail.osu.edu', 
        validators=[RegexValidator(EMAIL_VALIDATION, "Email must be of the form [name].#@buckeyemail.osu.edu")])
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
class ApplicationForm(forms.Form):
    in_columbus = forms.IntegerField()
    previous_grader = forms.IntegerField()
    prev_class = forms.CharField(max_length=4, required=False)
    preferred_class_1 = forms.CharField(max_length=15)
    preferred_class_instr_1 = forms.CharField(max_length=40, required=False)
    preferred_class_2 = forms.CharField(max_length=15, required=False)
    preferred_class_instr_2 = forms.CharField(max_length=40, required=False)
    preferred_class_3 = forms.CharField(max_length=15, required=False)
    preferred_class_instr_3 = forms.CharField(max_length=40, required=False)
