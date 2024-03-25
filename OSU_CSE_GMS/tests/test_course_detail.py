from django.test import TestCase

from OSU_CSE_GMS.models import Course, Section, User, Administrator

ADMIN_FORM_URL = '/administrator/courses/{}/'

class AdministratorTests(TestCase):
    def setUp(self):
        # Create a course
        self.course = Course.objects.create(course_number='2431', name='Systems II: Introduction to Operating Systems')

    def test_add_section_creates_section(self):
        section_data = {
            'add_section' : ['add_section'],
            'course_number' : ['2431'],
            'section_number' : ['1'],
            'semester' : ['SP2024'],
            'instruction_mode' : ['SYNCHRONOUS'],
            'time' : ['10:20-11:15'],
            'days_of_week' : ['MWF'],
            'classroom' : ['Dreese Lab 100'],
            'num_graders_needed' : ['2']
        }

        # Track number of sections in DB before POST
        num_sections_before = Section.objects.all().count()

        # Construct URL with course number
        url = ADMIN_FORM_URL.format('2431')

        # Make POST
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data=section_data, follow=True)

        # Print form errors for debugging
        print(response.context['section_form'].errors)

        # Assert the form is valid
        self.assertTrue(response.context['section_form'].is_valid())

        # Assert the number of sections in the DB increased by 1
        num_sections_after = Section.objects.all().count()
        self.assertEqual(num_sections_after, num_sections_before + 1)

        # Validate the section object is created as intended
        course = Course.objects.get(course_number='2431')
        section = Section.objects.get(section_number='1', course_number=course.course_number, semester='SP2024')

        self.assertEqual(course.course_number, '2431')
        self.assertEqual(section.section_number, '1')
        self.assertEqual(section.semester, 'SP2024')
        self.assertEqual(section.instruction_mode, 'SYNCHRONOUS')
        self.assertEqual(section.time, '10:20-11:15')
        self.assertEqual(section.days_of_week, 'MWF')
        self.assertEqual(section.classroom, 'Dreese Lab 100')
        self.assertEqual(section.num_graders_needed, 2)

    def test_edit_section_modifies_section(self):
        # Add section to the database
        new_section = Section.objects.create(
            course_number=self.course,
            section_number='1',
            semester='SP2024',
            instruction_mode='SYNCHRONOUS',
            time='10:20-11:15',
            days_of_week='MWF',
            classroom='Dreese Lab 100',
            num_graders_needed=2
        )

        # Make POST request to update the section
        section_data = {
            'update_section' : ['update_section'],
            'course_number' : ['2431'],
            'section_number' : ['1'],
            'semester' : ['SP2024'],
            'instruction_mode' : ['SYNCHRONOUS'],
            'time' : ['9:10-10:05'],
            'days_of_week' : ['MWF'],
            'classroom' : ['Dreese Lab 200'],
            'num_graders_needed' : ['2']
        }

        url = ADMIN_FORM_URL.format('2431')
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data=section_data, follow=True)

        # Verify the section was changed
        self.assertTrue(response.context['section_form'].is_valid())        
        updated_section = Section.objects.get(pk=new_section.pk)

        self.assertEqual(updated_section.course_number, self.course)
        self.assertEqual(updated_section.section_number, '1')
        self.assertEqual(updated_section.semester, 'SP2024')
        self.assertEqual(updated_section.instruction_mode, 'SYNCHRONOUS')
        self.assertEqual(updated_section.time, '9:10-10:05')
        self.assertEqual(updated_section.days_of_week, 'MWF')
        self.assertEqual(updated_section.classroom, 'Dreese Lab 200')
        self.assertEqual(updated_section.num_graders_needed, 2)

    def test_delete_course_removes_course(self):
        # Add Section to the database
        Section.objects.create(
            course_number=self.course,
            section_number='1',
            semester='SP2024',
            instruction_mode='SYNCHRONOUS',
            time='10:20-11:15',
            days_of_week='MWF',
            classroom='Dreese Lab 100',
            num_graders_needed=2
        )

        # Make POST request to delete the section
        section_data = {
            'delete_section' : ['delete_section'],
            'course_number' : ['2431'],
            'section_number' : ['1'],
            'semester' : ['SP2024']
        }

        url = ADMIN_FORM_URL.format('2431')
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        admin = Administrator.objects.create(user=user, email ='test@example.com' )
        self.client.login(username='testuser', password='testpassword')
        self.client.post(url, data=section_data, follow=True)

        # Verify the section was deleted
        section = Section.objects.filter(course_number=self.course, section_number='1', semester='SP2024')
        self.assertFalse(section.exists())
            