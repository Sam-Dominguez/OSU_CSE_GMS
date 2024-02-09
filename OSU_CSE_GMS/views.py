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

    # Pass the form and courses to the template context
    context = {
        'form': form,
        'courses': courses,
    }
    
    return render(request, 'administrator.html', context)