from django.test import TestCase
from django.contrib.auth.models import User
from OSU_CSE_GMS.models import Student, Instructor, Administrator
from ..services import permissions

APPLICATION_FORM_URL = '/application/'
STUDENT_DASH_URL = '/student/'
ADMINISTRATOR_DASH_URL = '/administrator/courses/'
ADMINISTRATOR_CREATE_URL = '/administrator/create/'
INSTRUCTOR_GRADER_REQUEST_URL = '/instructor/'
OKAY_RESPONSE_CODE = 200
REDIRECT_RESPONSE_CODE = 302
FORBIDDEN_RESPONSE_CODE = 403

class PermissionTests(TestCase):

    def setUp(self):
        user_instructor = User.objects.create_user(username='testInstructor', password='12345')
        user_student = User.objects.create_user(username='testStudent', password='12345')
        user_admin = User.objects.create_user(username='testAdmin', password='12345')

        instructor = Instructor(first_name='Test', last_name='Instructor', email='testInstructor.250@osu.edu', user_id=user_instructor.id)
        instructor.save()

        student = Student(first_name='Test', last_name='Student', email='testStudent.500@buckeyemail.osu.edu', user_id=user_student.id)
        student.save()

        admin = Administrator(first_name='Test', last_name='Admin', email='testAdmin.750@buckeyemail.osu.edu', user_id=user_admin.id)
        admin.save()


    def test_created_student_has_student_group_and_not_instructor_and_not_administrator(self):
        student_user = User.objects.filter(username='testStudent')

        self.assertTrue(student_user.exists())

        student_user = student_user[0]

        self.assertTrue(permissions.has_group(student_user, permissions.STUDENT_GROUP))
        self.assertFalse(permissions.has_group(student_user, permissions.INSTRUCTOR_GROUP))
        self.assertFalse(permissions.has_group(student_user, permissions.ADMINISTRATOR_GROUP))

    def test_created_instructor_has_instructor_group_and_not_student_and_not_administrator(self):
        instructor_user = User.objects.filter(username='testInstructor')

        self.assertTrue(instructor_user.exists())

        instructor_user = instructor_user[0]

        self.assertTrue(permissions.has_group(instructor_user, permissions.INSTRUCTOR_GROUP))
        self.assertFalse(permissions.has_group(instructor_user, permissions.STUDENT_GROUP))
        self.assertFalse(permissions.has_group(instructor_user, permissions.ADMINISTRATOR_GROUP))

    def test_created_administrator_has_administrator_group_and_not_student_and_not_instructor(self):
        administrator_user = User.objects.filter(username='testAdmin')

        self.assertTrue(administrator_user.exists())

        administrator_user = administrator_user[0]

        self.assertTrue(permissions.has_group(administrator_user, permissions.ADMINISTRATOR_GROUP))
        self.assertFalse(permissions.has_group(administrator_user, permissions.STUDENT_GROUP))
        self.assertFalse(permissions.has_group(administrator_user, permissions.INSTRUCTOR_GROUP))


    # Super User
    def test_superuser_can_access_all_gated_pages(self):
        User.objects.create_superuser(username='superuser', password='superuserpw')

        self.client.login(username='superuser', password='superuserpw')

        self.assertNotEqual(self.client.get(APPLICATION_FORM_URL).status_code, FORBIDDEN_RESPONSE_CODE)
        self.assertNotEqual(self.client.get(STUDENT_DASH_URL).status_code, FORBIDDEN_RESPONSE_CODE)
        self.assertNotEqual(self.client.get(ADMINISTRATOR_DASH_URL).status_code, FORBIDDEN_RESPONSE_CODE)
        self.assertNotEqual(self.client.get(ADMINISTRATOR_CREATE_URL).status_code, FORBIDDEN_RESPONSE_CODE)
        self.assertNotEqual(self.client.get(INSTRUCTOR_GRADER_REQUEST_URL).status_code, FORBIDDEN_RESPONSE_CODE) 

    # Application

    def test_student_can_view_application(self):
        # Login as a student
        self.client.login(username='testStudent', password='12345')

        # Try to view application page
        response = self.client.get(APPLICATION_FORM_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, OKAY_RESPONSE_CODE)

    def test_administrator_cannot_view_application(self):
        # Login as a student
        self.client.login(username='testAdmin', password='12345')

        # Try to view application page
        response = self.client.get(APPLICATION_FORM_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)

    def test_instructor_cannot_view_application(self):
        # Login as a student
        self.client.login(username='testInstructor', password='12345')

        # Try to view application page
        response = self.client.get(APPLICATION_FORM_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)


    # Student Dashboard

    def test_student_can_view_student_dashboard(self):
        # Login as a student
        self.client.login(username='testStudent', password='12345')

        # Try to view application page
        response = self.client.get(STUDENT_DASH_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, OKAY_RESPONSE_CODE)

    def test_administrator_cannot_view_student_dashboard(self):
        # Login as a student
        self.client.login(username='testAdmin', password='12345')

        # Try to view application page
        response = self.client.get(STUDENT_DASH_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)

    def test_instructor_cannot_view_student_dashboard(self):
        # Login as a student
        self.client.login(username='testInstructor', password='12345')

        # Try to view application page
        response = self.client.get(STUDENT_DASH_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)


    # Admin Dashboard

    def test_administrator_can_view_admin_dashboard(self):
        # Login as a student
        self.client.login(username='testAdmin', password='12345')

        # Try to view application page
        response = self.client.get(ADMINISTRATOR_DASH_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, OKAY_RESPONSE_CODE)

    def test_student_cannot_view_admin_dashboard(self):
        # Login as a student
        self.client.login(username='testStudent', password='12345')

        # Try to view application page
        response = self.client.get(ADMINISTRATOR_DASH_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)

    def test_instructor_cannot_view_admin_dashboard(self):
        # Login as a student
        self.client.login(username='testInstructor', password='12345')

        # Try to view application page
        response = self.client.get(ADMINISTRATOR_DASH_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)


    # Create Admin

    def test_administrator_can_view_create_admin(self):
        # Login as a student
        self.client.login(username='testAdmin', password='12345')

        # Try to view application page
        response = self.client.get(ADMINISTRATOR_CREATE_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, OKAY_RESPONSE_CODE)
        
    def test_student_cannot_view_create_admin(self):
        # Login as a student
        self.client.login(username='testStudent', password='12345')

        # Try to view application page
        response = self.client.get(ADMINISTRATOR_CREATE_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)

    def test_instructor_cannot_view_create_admin(self):
        # Login as a student
        self.client.login(username='testInstructor', password='12345')

        # Try to view application page
        response = self.client.get(ADMINISTRATOR_CREATE_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)

    
    # Grader Request Form
        
    def test_instructor_can_view_grader_request(self):
        # Login as a student
        self.client.login(username='testInstructor', password='12345')

        # Try to view application page
        response = self.client.get(INSTRUCTOR_GRADER_REQUEST_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, OKAY_RESPONSE_CODE)
    
    def test_student_cannot_view_grader_request(self):
        # Login as a student
        self.client.login(username='testStudent', password='12345')

        # Try to view application page
        response = self.client.get(INSTRUCTOR_GRADER_REQUEST_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)
        
    def test_administrator_cannot_view_grader_request(self):
        # Login as a student
        self.client.login(username='testAdmin', password='12345')

        # Try to view application page
        response = self.client.get(INSTRUCTOR_GRADER_REQUEST_URL)

        # Assert 200 status code
        self.assertEqual(response.status_code, FORBIDDEN_RESPONSE_CODE)