from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.defaults import server_error
from .forms import CourseForm, SignUpForm
from .models import Course, Student, Assignment, Section

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
    # Get signed in user
    user = request.user

    # Get associated student object
    student = Student.objects.filter(user_id=user.id)

    if not student.exists():
        # Handle case where student and user are not propery linked
        print(f'ERROR: The student linked with user id: {user.id} does not exist.')
        return server_error(request, '500.html')
    else:
        student = student[0]
        # Get assignment(s)
        assignments_objects = Assignment.objects.filter(student_id_id=student.id, status='ACCEPTED')
        assignments = list(assignments_objects)

        assigned_sections = []

        # Add the section objects related to the assignments to a list
        for assignment in assignments:
            section_objects = Section.objects.filter(section_number=assignment.section_number_id)
            if section_objects.exists():
                section = section_objects[0]
                # get course related to section
                course_object = Course.objects.filter(course_number=section.course_number_id)

                if not course_object.exists():
                    print("Course does not exist")
                else:
                    assigned_sections.append((course_object[0], section))
                

        context = {
            'user' : user,
            'student' : student,
            'assignments' : dict(assigned_sections)
        }

        return render(request, 'student.html', context)
