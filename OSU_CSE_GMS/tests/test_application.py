from django.test import TestCase
from django.contrib.auth.models import User
from OSU_CSE_GMS.models import Student, UnassignedStudent, PreviousClassTaken, Course, Assignment, Instructor, Section

APPLICATION_FORM_URL = '/application/'
THANKS_PAGE_URL = '/thanks/'
SIGNUP_FORM_URL = '/sign_up/'

class ApplicationTests(TestCase):
    
    
    def setUp(self):
        user_instructor = User.objects.create_user(username='testInstructor', password='12345')
        user_student = User.objects.create_user(username='testStudent', password='12345')

        instructor = Instructor(first_name='Test', last_name='Instructor', email='testInstructor.250@osu.edu', user_id=user_instructor.id)
        instructor.save()

        student = Student(first_name='Test', last_name='Student', email='testStudent.500@buckeyemail.osu.edu', user_id=user_student.id)
        student.save()

        Course.objects.create(course_number='2221', name='Software 1: Software Components')

        section = Section(section_number='10021', instruction_mode='SYNCHRNONOUS', semester='AU24', time='11:30-12:25', 
                days_of_week='MWF', classroom='Dreese Lab 300', course_number_id='2221', instructor_id=instructor.id)
        section.save()
    
    def test_submission_updates_student(self): 
        application_data = {
            'in_columbus' : [1],
            'previous_grader' : [1],
            'prev_class': ['2221'],
            'preferred_class_1' : ['2221']
        }
        
        self.client.login(username='testStudent', password='12345')
        
        response = self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
        
        # print(response.context)
        # self.assertIn('application_form', response.context)
        # self.assertTrue(response.context['application_form'].is_valid())
        student = Student.objects.get(first_name='Test')
        
        self.assertNotEqual(student.in_columbus, None)
        self.assertEqual(student.in_columbus, 1)
        self.assertNotEqual(student.previous_grader, None)
        self.assertEqual(student.previous_grader, 1)
        self.assertNotEqual(student.graded_last_term, None)
        self.assertEqual(student.graded_last_term, '2221')
        self.assertRedirects(response, THANKS_PAGE_URL)
        
    # def test_submission_adds_course_no_instructor(self):
        
    #     # new_course = Course(course_number='2221', name='Software 1: Software Components')
    #     # new_course.save()
        
    #     application_data = {
    #         'in_columbus' : [1],
    #         'previous_grader' : [1],
    #         'prev_class': ['2221'],
    #         'preferred_class_1' : ['2221'],
    #     }
        
    #     courses_before = PreviousClassTaken.objects.all().count()
    #     print(Course.objects.all().count())
    #     response = self.client.post(APPLICATION_FORM_URL, data=application_data, follow=True)
    #     courses_after = PreviousClassTaken.objects.all().count()
        
    #     self.assertEquals(courses_after, courses_before + 1)
    #     # self.assertTrue(response.context['form'].is_valid())