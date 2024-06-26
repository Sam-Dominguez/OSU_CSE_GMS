from django.test import TestCase
from django.contrib.auth.models import User
from OSU_CSE_GMS.models import Student, PreviousClassTaken, Course, Instructor, Section

APPLICATION_FORM_URL = '/student/application/'
THANKS_PAGE_URL = '/thanks/'

class ApplicationTests(TestCase):

    def setUp(self):
        user_instructor = User.objects.create_user(username='testInstructor', password='12345')
        user_student = User.objects.create_user(username='testStudent', password='12345')

        instructor = Instructor(first_name='Test', last_name='Instructor', email='testInstructor.250@osu.edu', user_id=user_instructor.id)
        instructor.save()

        student = Student(first_name='Test', last_name='Student', email='testStudent.500@buckeyemail.osu.edu', user_id=user_student.id)
        student.save()
        self.student = student

        Course.objects.create(course_number='2221', name='Software 1: Software Components')
        Course.objects.create(course_number='3901', name='Project: Design, Development, and Documentation of Web Applications')
        Course.objects.create(course_number='1222', name='Introduction to Computer Programming in C++ for Engineers and Scientists')
        Course.objects.create(course_number='1110', name='Introduction to Computing Technology ')
        Course.objects.create(course_number='3902', name='Project: Design, Development, and Documentation of Interactive Systems')

        section = Section(section_number='10021', instruction_mode='SYNCHRONOUS', semester='AU24', time='11:30-12:25', 
                days_of_week='MWF', classroom='Dreese Lab 300', course_number_id='2221', instructor_id=instructor.id)
        section.save()

    def test_submission_updates_student(self): 
        application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2221']
        }
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Make POST
        response = self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
        
        # Get student record from DB
        student = Student.objects.get(first_name='Test')
        
        # Check that record has been updated
        self.assertNotEqual(student.in_columbus, None)
        self.assertEqual(student.in_columbus, 1)
        self.assertNotEqual(student.previous_grader, None)
        self.assertEqual(student.previous_grader, 1)
        self.assertNotEqual(student.graded_last_term, None)
        self.assertEqual(student.graded_last_term, '2221')
        self.assertRedirects(response, THANKS_PAGE_URL)

    def test_submission_adds_course_no_instructor(self):
        application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2221'],
        }
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Track number of application courses in DB before POST
        courses_before = PreviousClassTaken.objects.all().count()
        
        # Make POST
        self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
        
        # Track number of application courses in DB after POST and ensure one was created
        courses_after = PreviousClassTaken.objects.all().count()
        self.assertEqual(courses_after, courses_before + 1)
        
        # Validate record is created as intended
        previousClass = PreviousClassTaken.objects.get(course_number='2221')
        
        # Validate no instructor
        self.assertEqual(previousClass.instructor, '')

    def test_submission_adds_course_with_instructor(self):
        application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2221'],
            'preferred_class_instr_1' : ['Jones.1'],
        }
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Track number of application courses in DB before POST
        courses_before = PreviousClassTaken.objects.all().count()
        
        # Make POST
        self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
        
        # Track number of application courses in DB after POST and ensure one was created
        courses_after = PreviousClassTaken.objects.all().count()
        self.assertEqual(courses_after, courses_before + 1)
        
        # Validate record is created as intended
        previousClass = PreviousClassTaken.objects.get(course_number='2221')
        
        # Validate instructor
        self.assertEqual(previousClass.instructor, 'Jones.1')
        
    def test_submission_no_course_added_incorrect_course_info(self):
        application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2212'],
            'preferred_class_instr_1' : ['Jones.1'],
        }
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Track number of application courses in DB before POST
        courses_before = PreviousClassTaken.objects.all().count()
        
        # Make POST
        self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
        
        # Track number of application courses in DB after POST and ensure none were created
        courses_after = PreviousClassTaken.objects.all().count()
        self.assertEqual(courses_after, courses_before)
        
    def test_submission_adds__all_courses(self):
        application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2221'],
            'preferred_class_instr_1' : ['Jones.1'],
            'preferred_class_2' : ['3901'],
            'preferred_class_instr_2' : ['Smith.201'],
            'preferred_class_3' : ['1222'],
        }
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Track number of application courses in DB before POST
        courses_before = PreviousClassTaken.objects.all().count()
        
        # Make POST
        self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
        
        # Track number of application courses in DB after POST and ensure they were created
        courses_after = PreviousClassTaken.objects.all().count()
        self.assertEqual(courses_after, courses_before + 3)
        
        # Validate record is created as intended
        previousClass1 = PreviousClassTaken.objects.get(course_number='2221')
        previousClass2 = PreviousClassTaken.objects.get(course_number='3901')
        previousClass3 = PreviousClassTaken.objects.get(course_number='1222')
        
        # Validate instructors
        self.assertEqual(previousClass1.instructor, 'Jones.1')
        self.assertEqual(previousClass2.instructor, 'Smith.201')
        self.assertEqual(previousClass3.instructor, '')
        
    def test_edit_submission(self):
        previous_application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2221'],
            'preferred_class_instr_1' : ['Jones.1'],
            'preferred_class_2' : ['3901'],
            'preferred_class_instr_2' : ['Smith.201'],
            'preferred_class_3' : ['1222'],
        }
        edited_application_data = {
            'in_columbus' : [0],
            'previous_grader' : [0],
            'prev_class': ['1110'],
            'preferred_class_1' : ['1110'],
            'preferred_class_instr_1' : ['Jackson.2'],
            'preferred_class_2' : ['3902'],
        }

        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Save previous application
        self.client.post(APPLICATION_FORM_URL, data=previous_application_data, follow=True)
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Make POST to edit student data
        self.client.post(APPLICATION_FORM_URL, data=edited_application_data, follow=True)
        
        # Validate record is created as intended
        previousClass1 = PreviousClassTaken.objects.get(course_number='1110')
        previousClass2 = PreviousClassTaken.objects.get(course_number='3902')
        
        # Validate instructors
        self.assertEqual(previousClass1.instructor, 'Jackson.2')
        self.assertEqual(previousClass2.instructor, '')

        # Get student object from DB
        student = Student.objects.get(email='testStudent.500@buckeyemail.osu.edu')
        
        # Validate student data was updated
        self.assertEqual(student.in_columbus, 0)
        self.assertEqual(student.previous_grader, 0)
        self.assertEqual(student.graded_last_term, '1110')

    def test_edit_submission_reordered_preferences(self):
        previous_application_data = {
            'in_columbus' : [1],
            'previous_grader' : [0],
            'preferred_class_1' : ['2221'],
            'preferred_class_2' : ['3901'],
            'preferred_class_3' : ['1222'],
        }
        edited_application_data = {
            'in_columbus' : [1],
            'previous_grader' : [0],
            'preferred_class_1' : ['3901'],
            'preferred_class_2' : ['1222'],
            'preferred_class_3' : ['2221'],
        }

        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Save previous application
        self.client.post(APPLICATION_FORM_URL, data=previous_application_data, follow=True)

        # Validate record is created as intended
        previousClass1 = PreviousClassTaken.objects.get(course_number='2221')
        previousClass2 = PreviousClassTaken.objects.get(course_number='3901')
        previousClass3 = PreviousClassTaken.objects.get(course_number='1222')
        
        # Validate pref number
        self.assertEqual(previousClass1.pref_num, 1)
        self.assertEqual(previousClass2.pref_num, 2)
        self.assertEqual(previousClass3.pref_num, 3)

        # Validate student
        self.assertEqual(previousClass1.student_id, self.student)
        self.assertEqual(previousClass2.student_id, self.student)
        self.assertEqual(previousClass3.student_id, self.student)
        
        # Login to access page
        self.client.login(username='testStudent', password='12345')
        
        # Make POST to edit student data
        self.client.post(APPLICATION_FORM_URL, data=edited_application_data, follow=True)
        
        # Validate record is created as intended
        previousClass1 = PreviousClassTaken.objects.get(course_number='3901')
        previousClass2 = PreviousClassTaken.objects.get(course_number='1222')
        previousClass3 = PreviousClassTaken.objects.get(course_number='2221')
        
        # Validate pref number
        self.assertEqual(previousClass1.pref_num, 1)
        self.assertEqual(previousClass2.pref_num, 2)
        self.assertEqual(previousClass3.pref_num, 3)

        # Validate student
        self.assertEqual(previousClass1.student_id, self.student)
        self.assertEqual(previousClass2.student_id, self.student)
        self.assertEqual(previousClass3.student_id, self.student)

        # Get student object from DB
        student = Student.objects.get(email='testStudent.500@buckeyemail.osu.edu')
        
        # Validate student data was updated
        self.assertEqual(student.in_columbus, 1)
        self.assertEqual(student.previous_grader, 0)
        self.assertEqual(student.graded_last_term, '')