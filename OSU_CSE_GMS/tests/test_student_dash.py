from django.test import TestCase

from OSU_CSE_GMS.models import Student, UnassignedStudent, Assignment, Course, Section, User, Instructor

STUDENT_URL = '/student/dashboard/'
REDIRECT_URL = '/accounts/login/?next=' + STUDENT_URL

class StudentDashboard(TestCase):

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

        self.assignment = Assignment.objects.create(section_number_id=section.id, student_id_id=student.id)

    # Test not logged in users are redirected to login
    def test_not_logged_in_users_redirected_to_login(self):
        response = self.client.get(STUDENT_URL, follow=True)

        self.assertRedirects(response, REDIRECT_URL)

    def test_reject_assignment_deletes_assignment_and_adds_student_to_unassigned_table_bad_assignment_reason_given(self):
        assignment_rejection = {
            'reject_assignment' : ['reject_assignment'],
            'rejection_reason': ['bad-assignment'],
            'other_reason': ['I do not work well with test instructor'],
            'assignment_id' : ['1'],
            'student_id' : ['1']
        }

        # Login Student
        self.client.login(username='testStudent', password='12345')

        # Get initial value of num_graders_needed
        section = Section.objects.get(id='1')
        num_graders_needed = section.num_graders_needed

        # Reject assignment
        self.client.post(STUDENT_URL, data=assignment_rejection)

        # Check that the assignment was deleted
        assignment = Assignment.objects.filter(id='1')
        self.assertFalse(assignment.exists())
        
        # Check that the student was added to the unassigned students table
        unassigned_student = UnassignedStudent.objects.filter(student_id_id='1')

        self.assertTrue(unassigned_student.exists())
        unassigned_student_entry = unassigned_student[0]

        self.assertEqual(unassigned_student_entry.student_id_id, 1)

        # Check that the num_graders_needed was incremented
        updated_section = Section.objects.get(id='1')
        updated_num_graders_needed = updated_section.num_graders_needed
        
        self.assertEqual(updated_num_graders_needed, num_graders_needed + 1)

    def test_reject_assignment_deletes_assignment_dont_reassign_given(self):
        assignment_rejection = {
            'reject_assignment' : ['reject_assignment'],
            'rejection_reason': ['dont-reassign'],
            'other_reason': [''],
            'assignment_id' : ['1'],
            'student_id' : ['1']
        }

        # Login Student
        self.client.login(username='testStudent', password='12345')

        # Get initial value of num_graders_needed
        section = Section.objects.get(id='1')
        num_graders_needed = section.num_graders_needed

        # Reject assignment
        self.client.post(STUDENT_URL, data=assignment_rejection)

        # Check that the assignment was deleted
        assignment = Assignment.objects.filter(id='1')
        self.assertFalse(assignment.exists())
        
        # Check that the student was NOT added to the unassigned students table
        unassigned_student = UnassignedStudent.objects.filter(student_id_id='1')
        self.assertFalse(unassigned_student.exists())

        # Check that the num_graders_needed was incremented
        updated_section = Section.objects.get(id='1')
        updated_num_graders_needed = updated_section.num_graders_needed
        
        self.assertEqual(updated_num_graders_needed, num_graders_needed + 1)