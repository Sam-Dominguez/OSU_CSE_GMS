from django.test import TestCase
from django.contrib.auth.models import User
from OSU_CSE_GMS.models import Student, Course, Assignment, Instructor, Section

INSTRUCTOR_FORM_URL = '/instructor/'
THANKS_PAGE_URL = '/thanks/'

class InstructorTests(TestCase):

    def setUp(self):
        user_instructor = User.objects.create_user(username='testInstructor', password='12345')
        user_student = User.objects.create_user(username='testStudent', password='12345')

        instructor = Instructor(first_name='Test', last_name='Instructor', email='testInstructor.250@osu.edu', user_id=user_instructor.id)
        instructor.save()

        student = Student(first_name='Test', last_name='Student', email='testStudent.500@buckeyemail.osu.edu', user_id=user_student.id)
        student.save()

        Course.objects.create(course_number='2221', name='Software 1: Software Components')

        section = Section(section_number='10021', instruction_mode='SYNCHRONOUS', semester='AU24', time='11:30-12:25', 
                days_of_week='MWF', classroom='Dreese Lab 300', course_number_id='2221', instructor_id=instructor.id)
        section.save()
        
        # Assignment.objects.create(section_number_id=section.id, student_id_id=student.id)
        
    def test_submission_creates_assignment(self):
        teacher_input_data = {
            'section_number' : ['10021'],
            'student_email' : ['testStudent.500@buckeyemail.osu.edu'],
        }
        
        #Login to access page
        self.client.login(username='testInstructor', password='12345')
        
        # Track number of assignments prior to POST
        self.assertEqual(Assignment.objects.all().count(), 0)
        
        # Make POST
        response = self.client.post(INSTRUCTOR_FORM_URL, data=teacher_input_data, follow=True)
        
        # Check that assignment was created
        self.assertEqual(Assignment.objects.all().count(), 1)
        
        # Get assignment record from DB
        section = Section.objects.get(section_number='10021')
        assignment = Assignment.objects.get(section_number=section)
        
        # Get records for comparison
        student = Student.objects.get(email='testStudent.500@buckeyemail.osu.edu')
        course = Course.objects.get(course_number='2221')
        
        # Validate assignment data
        self.assertEqual(assignment.section_number, section)
        self.assertEqual(assignment.student_id, student)
        self.assertEqual(assignment.section_number.course_number, course)
        self.assertRedirects(response, THANKS_PAGE_URL)
        
    def test_nonexistent_section_does_not_create_assignment(self):
        teacher_input_data = {
            'section_number' : [''],
            'student_email' : ['testStudent.500@buckeyemail.osu.edu'],
        }
        
        #Login to access page
        self.client.login(username='testInstructor', password='12345')
        
        # Track number of assignments prior to POST
        self.assertEqual(Assignment.objects.all().count(), 0)
        
        # Make POST
        response = self.client.post(INSTRUCTOR_FORM_URL, data=teacher_input_data, follow=True)
        
        # Check that assignment was not created
        self.assertEqual(Assignment.objects.all().count(), 0)
        
    def test_nonexistent_student_does_not_create_assignment(self):
        teacher_input_data = {
            'section_number' : ['10021'],
            'student_email' : [''],
        }
        
        #Login to access page
        self.client.login(username='testInstructor', password='12345')
        
        # Track number of assignments prior to POST
        self.assertEqual(Assignment.objects.all().count(), 0)
        
        # Make POST
        response = self.client.post(INSTRUCTOR_FORM_URL, data=teacher_input_data, follow=True)
        
        # Check that assignment was not created
        self.assertEqual(Assignment.objects.all().count(), 0)

