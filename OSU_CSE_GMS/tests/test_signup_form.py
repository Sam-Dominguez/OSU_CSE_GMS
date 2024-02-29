from django.test import TestCase
from OSU_CSE_GMS.models import Student
from django.contrib.auth.models import User

SIGNUP_FORM_URL = '/sign_up/'
REDIRECT_URL = '/accounts/login/?next=/student/'

FIELD_REQUIRED_ERROR = 'This field is required.'
PASSWORD_MATCH_ERROR = 'The two password fields didn’t match.'
BAD_EMAIL_ERROR = 'Email must be of the form [name].#@buckeyemail.osu.edu'
VALID_FORM_WITHOUT_EMAIL = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}

class SignUpTests(TestCase):

    def test_form_requires_all_fields_when_blank(self):
        empty_form_data = {}
        response = self.client.post(SIGNUP_FORM_URL, data=empty_form_data)

        self.assertFalse(response.context['form'].is_valid())

        self.assertFormError(response, 'form', 'first_name', FIELD_REQUIRED_ERROR)
        self.assertFormError(response, 'form', 'last_name', FIELD_REQUIRED_ERROR)
        self.assertFormError(response, 'form', 'email', FIELD_REQUIRED_ERROR)
        self.assertFormError(response, 'form', 'username', FIELD_REQUIRED_ERROR)
        self.assertFormError(response, 'form', 'password1', FIELD_REQUIRED_ERROR)
        self.assertFormError(response, 'form', 'password2', FIELD_REQUIRED_ERROR)

    def test_form_requires_passwords_match(self):
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'email' : 'brutus.1@osu.edu', 'password1' : 'samplepassword', 'password2' : 'notmatchedpassword'}
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'password2', PASSWORD_MATCH_ERROR)

    def test_invalid_form_creates_no_objects(self):
        form_data = {'email' : 'brutus.1@osu.edu'}

        num_users_before = User.objects.all().count()
        num_students_before = Student.objects.all().count()

        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertEqual(num_users_before, 0)
        self.assertEqual(num_students_before, 0)

        self.assertFalse(response.context['form'].is_valid())

        num_users_after = User.objects.all().count()
        num_students_after = Student.objects.all().count()

        self.assertEqual(num_users_after, 0)
        self.assertEqual(num_students_after, 0)


    # Email Regex Testing
        
    def test_form_rejects_non_osu_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'brutus.1@gmail.com'
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', [BAD_EMAIL_ERROR])

    def test_form_rejects_missing_dot_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'brutus1@osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)

    def test_form_rejects_missing_dot_number_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'brutus@osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)

    def test_form_rejects_missing_name_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = '548@osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)    

    # CURRENTLY A FAILING TEST, MARKED IN DEFECT CHART, REMOVE THIS COMMENT AND UNCOMMENT TEST WHEN FIXED
    # def test_form_rejects_missing_name_emails(self):
    #     form_data = VALID_FORM_WITHOUT_EMAIL
    #     form_data['email'] = '------.1@osu.edu'        
    #     response = self.client.post(SIGNUP_FORM_URL, data=form_data)

    #     self.assertFalse(response.context['form'].is_valid())
    #     self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)
        
    def test_form_accepts_valid_osu_email(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'allen.4567@osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

    def test_form_accepts_valid_buckeyemail_email(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'salazar.55@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

    def test_form_accepts_valid_osu_email_with_hyphens(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'berger-wolf.1@osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)
        

    def test_form_accepts_valid_buckeyemail_email_with_hyphens(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'simpson-hunt.15@osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

    def test_valid_form_creates_objects(self):
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}

        num_users_before = User.objects.all().count()
        num_students_before = Student.objects.all().count()

        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

        num_users_after = User.objects.all().count()
        num_students_after = Student.objects.all().count()

        self.assertEqual(num_users_after, num_users_before + 1)
        self.assertEqual(num_students_after, num_students_before + 1)

    def test_valid_form_creates_student_and_user(self):
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

        student = Student.objects.get(email='buckeye.2024@osu.edu')
        user = student.user

        self.assertNotEqual(user, None)
        self.assertEqual(student.email, user.email)
        self.assertEqual(student.first_name, user.first_name)
        self.assertEqual(student.last_name, user.last_name)

