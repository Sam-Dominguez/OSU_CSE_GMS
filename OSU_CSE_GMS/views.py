from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
from .models import Course

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

@login_required
def student(request):
    return render(request, 'student.html')
