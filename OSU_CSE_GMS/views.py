from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.defaults import server_error
from .forms import CourseForm, SectionForm, SignUpForm
from .models import Course, Student, Assignment, Section, UnassignedStudent, Instructor

def administrator(request):
    context = {}
    course_form = CourseForm()
    section_form = SectionForm()
    if request.method == 'POST':
        if 'add_course' in request.POST:
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course_form.save()
        elif 'update_course' in request.POST:
            course_number = request.POST['course_number']
            course = Course.objects.get(course_number=course_number)
            course_form = CourseForm(request.POST, instance=course)
            if course_form.is_valid():
                course_form.save()
        elif 'delete_course' in request.POST:
            course_number = request.POST['course_number']
            course = Course.objects.get(course_number=course_number)
            course.delete()
        elif 'add_section' in request.POST:
            section_form = SectionForm(request.POST)
            print(request.POST)
            if section_form.is_valid():
                section_form.save()
            else:
                print(section_form.errors)


    # Fetch all existing courses, sections, instructors from the database
    courses = Course.objects.all()
    sections = Section.objects.all()
    instructors = Instructor.objects.all()

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
        'course_form': course_form,
        'courses': courses,
        'section_form': section_form,
        'sections': sections,
        'instructors': instructors,
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
    if request.method == 'POST' and 'reject_assignment' in request.POST:
        # Delete the assignment
        assignment_id = request.POST['assignment_id']
        Assignment.objects.filter(id=assignment_id).delete()

        # Add the student back to the unassigned students table
        student_id = request.POST['student_id']
        UnassignedStudent(student_id_id=student_id).save()

    # Get signed in user
    user = request.user

    # Get associated student object
    student = Student.objects.filter(user_id=user.id)

    if not student.exists():
        # Handle case where student and user are not propery linked
        print(f'ERROR: The student linked with user id: {user.id} does not exist.')
        return server_error(request, '500.html')
    
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

            # Get instructor if they are in the database
            instructor = Instructor.objects.filter(id=section.instructor_id)
            instructor = instructor[0] if instructor.exists() else None

            # get course related to section
            course_object = Course.objects.filter(course_number=section.course_number_id)

            if not course_object.exists():
                print("Course does not exist")
            else:
                assigned_sections.append((assignment.id, (course_object[0], section, instructor)))

    context = {
        'user' : user,
        'student' : student,
        'assignments' : dict(assigned_sections)

    }

    return render(request, 'student.html', context)
