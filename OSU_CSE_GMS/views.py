from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CourseForm, SignUpForm
from .models import Course, Student, Section

def administrator(request):
    context = {}
    form = CourseForm()
    if request.method == 'POST':
        print(request.POST)
        if 'add_course' in request.POST:
            form = CourseForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'update_course' in request.POST:
            course_number = request.POST['course_number']
            course = Course.objects.get(course_number=course_number)
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
        elif 'delete_course' in request.POST:
            course_number = request.POST['course_number']
            course = Course.objects.get(course_number=course_number)
            course.delete()

    # Fetch all existing courses from the database
    courses = Course.objects.all()

    # Sort the courses by course_number
    sort_direction = 'asc'
    if 'sort' in request.GET:
        sort_direction = request.GET['sort']
        sort_direction = 'asc' if sort_direction == 'desc' else 'desc'

    if sort_direction == 'asc':
        courses = courses.order_by('course_number')
    else:
        courses = courses.order_by('-course_number')

    context = {
        'form': form,
        'courses': courses,
        'sort_direction': sort_direction,
    }
    
    return render(request, 'administrator.html', context)

def course_detail(request, course_number):
    course = Course.objects.get(course_number=course_number)
    sections = Section.objects.filter(course_number=course_number)
    context = {
        'course': course,
        'sections': sections
    }
    return render(request, 'course_detail.html', context)

def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.get(username=username)
            student = Student(user=user, email=email, first_name=first_name, last_name=last_name)
            student.save()
            return redirect('student')
        
    context = {
        'form' : form
    }

    return render(request, 'registration/signup.html', context)

@login_required
def student(request):
    return render(request, 'student.html')
