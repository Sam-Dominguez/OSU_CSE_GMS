from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CourseForm, SignUpForm
from .models import Course, Student

def administrator(request):
    context = {}
    form = CourseForm()
    if request.method == 'POST':
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
        sort_text = 'Sorting (asc)'
    else:
        courses = courses.order_by('-course_number')
        sort_text = 'Sorting (desc)'

    context = {
        'form': form,
        'courses': courses,
        'sort_direction': sort_direction,
        'sort_text': sort_text
    }
    
    return render(request, 'administrator.html', context)

def course_detail(request, course_number):
    course = Course.objects.get(course_number=course_number)
    context = {
        'course': course
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
import logging
import sys
from venv import logger
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import ClassPrefForm, GraderForm
from .models import Student

def test(request):
    context = {'form':GraderForm()}
    return render(request, 'user_intake/test.html', context)

def student_intake(request):
    context = {'form': GraderForm()}
    logger = logging.getLogger('django')
    if request.method == 'POST':
        form = GraderForm(request.POST)
        logger.info('checking validity')
        logger.info(form.errors)
        if form.is_valid():
            user = request.user
            id = form.cleaned_data.get('id')
            email = request.POST['name_num'] + '@buckeyemail.osu.edu'
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            in_columbus = request.POST['in_columbus']
            previous_grader = request.POST['previous_grader']
            previous_classes = 0
            grader = Student(id=id, user=user, email=email, first_name=first_name, last_name=last_name, in_columbus=in_columbus, previous_grader=previous_grader, previous_classes=previous_classes)
            logger.info('saving!')
            grader.save()
            # form.save()
            return redirect('/thanks/')
        else:
            context = {'messages': {"Form is invalid. Try again."}, 'form': GraderForm()}
    else:
        form = GraderForm()
    
    students = Student.objects.all()
    logger.info('This is students in DB')
    logger.info(students)
    return render(request, 'user_intake/application.html', context)

def create_course(request):
    if request.method == 'POST':
        pass
    return ren