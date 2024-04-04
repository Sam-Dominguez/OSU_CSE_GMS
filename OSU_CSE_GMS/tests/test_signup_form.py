from django.test import TestCase
from OSU_CSE_GMS.models import Student, Administrator, Instructor
from django.contrib.auth.models import User 

SIGNUP_FORM_URL = '/sign_up/'
CREATE_ADMIN_FORM_URL = '/administrator/create_admin/'
CREATE_INSTRUCTOR_FORM_URL = '/administrator/create_instructor/'
REDIRECT_URL = '/accounts/login/?next=/student/dashboard/'

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
        form_data['email'] = 'brutus1@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)

    def test_form_rejects_missing_dot_number_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'brutus@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)

    def test_form_rejects_missing_name_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = '548@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)    

    def test_form_rejects_missing_name_emails(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = '------.1@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data)

        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', BAD_EMAIL_ERROR)
        
    def test_form_accepts_valid_osu_email(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'allen.4567@buckeyemail.osu.edu'        
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
        form_data['email'] = 'berger-wolf.1@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)
        

    def test_form_accepts_valid_buckeyemail_email_with_hyphens(self):
        form_data = VALID_FORM_WITHOUT_EMAIL
        form_data['email'] = 'simpson-hunt.15@buckeyemail.osu.edu'        
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

    def test_valid_form_creates_objects(self):
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@buckeyemail.osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}

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
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@buckeyemail.osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}
        response = self.client.post(SIGNUP_FORM_URL, data=form_data, follow=True)

        # Assert that the form submitted successfully and redirects the user to login before going to the student dash
        self.assertRedirects(response, REDIRECT_URL)

        student = Student.objects.get(email='buckeye.2024@buckeyemail.osu.edu')
        user = student.user

        self.assertNotEqual(user, None)
        self.assertEqual(student.email, user.email)
        self.assertEqual(student.first_name, user.first_name)
        self.assertEqual(student.last_name, user.last_name)





#### Testing creating admin by admin ####
    def test_valid_form_creates_objects_admin(self):
        # log in does nothing now, future proofing so only admin logged in can create another admin
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')

        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}

        num_users_before = User.objects.all().count()
        num_admin_before = Administrator.objects.all().count()

        response = self.client.post(CREATE_ADMIN_FORM_URL, data=form_data, follow=True)

        num_users_after = User.objects.all().count()
        num_admin_after = Administrator.objects.all().count()

        self.assertEqual(num_users_after, num_users_before + 1)
        self.assertEqual(num_admin_after, num_admin_before + 1)

    def test_valid_form_creates_admin_and_user(self):
        # log in does nothing now, future proofing so only admin logged in can create another admin
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}
        response = self.client.post(CREATE_ADMIN_FORM_URL, data=form_data, follow=True)

  
        admin = Administrator.objects.get(email='buckeye.2024@osu.edu')
        user = admin.user

        self.assertNotEqual(user, None)
        self.assertEqual(admin.email, user.email)
        self.assertEqual(admin.first_name, user.first_name)
        self.assertEqual(admin.last_name, user.last_name)


#### Testing creating instructor by admin ####
    def test_valid_form_creates_objects_instructor(self):
        # log in does nothing now, future proofing so only admin logged in can create another admin
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')

        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}

        num_users_before = User.objects.all().count()
        num_instructor_before = Instructor.objects.all().count()

        response = self.client.post(CREATE_INSTRUCTOR_FORM_URL, data=form_data, follow=True)

        num_users_after = User.objects.all().count()
        num_instructor_after = Instructor.objects.all().count()

        self.assertEqual(num_users_after, num_users_before + 1)
        self.assertEqual(num_instructor_after, num_instructor_before + 1)

    def test_valid_form_creates_instructor_and_user(self):
        # log in does nothing now, future proofing so only admin logged in can create another admin
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')
        form_data = {'first_name' : 'Test FName', 'last_name' : 'Test LName', 'username' : 'MyUsername', 'email' : 'buckeye.2024@osu.edu', 'password1' : 'samplepassword', 'password2' : 'samplepassword'}
        response = self.client.post(CREATE_INSTRUCTOR_FORM_URL, data=form_data, follow=True)


        instructor = Instructor.objects.get(email='buckeye.2024@osu.edu')
        user = instructor.user

        self.assertNotEqual(user, None)
        self.assertEqual(instructor.email, user.email)
        self.assertEqual(instructor.first_name, user.first_name)
        self.assertEqual(instructor.last_name, user.last_name)