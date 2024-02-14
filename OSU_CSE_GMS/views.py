from django.shortcuts import render
from .forms import CourseForm
from .models import Course

def administrator(request):
    context = {}
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CourseForm()

    # Fetch all existing courses from the database
    courses = Course.objects.all()
    sort_direction = 'asc'

    # Toggle the sort direction
    if 'sort' in request.GET:
        sort_direction = request.GET['sort']
        sort_direction = 'asc' if sort_direction == 'desc' else 'desc'

    # Sort courses based on the sort direction
    if sort_direction == 'asc':
        courses = courses.order_by('course_number')
        sort_text = 'Sorting (asc)'
    else:
        courses = courses.order_by('-course_number')
        sort_text = 'Sorting (desc)'

    # Pass the form and courses to the template context
    context = {
        'form': form,
        'courses': courses,
        'sort_direction': sort_direction,
        'sort_text': sort_text
    }
    
    return render(request, 'administrator.html', context)