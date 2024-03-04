from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CourseForm, SignUpForm, ApplicationForm
from .models import Course, Student, PreviousClassTaken, UnassignedStudent
import logging

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

@login_required
def student_intake(request):
    context = {'form': ApplicationForm()}
    logger = logging.getLogger('django')
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        
        if form.is_valid():
            
            # Update student record in database
            student = Student.objects.filter(user_id=request.user.id)
            if student.exists():
                student = student[0]
                student.in_columbus = form.cleaned_data.get('in_columbus')
                student.previous_grader = form.cleaned_data.get('previous_grader')
                student.graded_last_term = form.cleaned_data.get('prev_class')
                logger.info('updating student record')
                student.save(update_fields=['in_columbus','previous_grader'])
            else:
                logger.error('Student does not exist in the database.')

            # Add student course preferences to database
            student = Student.objects.get(user_id=request.user)
            course_num_1 = form.cleaned_data.get('preferred_class_1')
            course_instr_1 = form.cleaned_data.get('preferred_class_instr_1')
            course1 = Course.objects.get(course_number=course_num_1)
            course_1_record = PreviousClassTaken(student_id=student, course_number=course1, instructor=course_instr_1, pref_num=1)
            course_1_record.save()
            course_num_2 = form.cleaned_data.get('preferred_class_2')
            course_instr_2 = form.cleaned_data.get('preferred_class_instr_2')
            course2 = Course.objects.get(course_number=course_num_2)
            course_2 = PreviousClassTaken(student_id=student, course_number=course2, instructor=course_instr_2, pref_num=2)
            course_2.save()
            course_num_3 = form.cleaned_data.get('preferred_class_3')
            course_instr_3 = form.cleaned_data.get('preferred_class_instr_3')
            course3 = Course.objects.get(course_number=course_num_3)
            course_3 = PreviousClassTaken(student_id=student, course_number=course3, instructor=course_instr_3, pref_num=3)
            course_3.save()   
            
            # Add student to unassigned students
            unassigned_student = UnassignedStudent(student_id=student)
            unassigned_student.save()
            
            return redirect('/thanks/')
        else:
            context = {'messages': {"Form is incomplete. Try again."}, 'form': ApplicationForm()}
    else:
        form = ApplicationForm()
    
    return render(request, 'user_intake/application.html', context)