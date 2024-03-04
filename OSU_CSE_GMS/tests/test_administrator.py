from django.test import TestCase

from OSU_CSE_GMS.models import Course

ADMIN_FORM_URL = '/administrator/courses/'

class AdministratorTests(TestCase):

    def test_add_course_creates_course(self):
        course_data = {
            'add_course' : ['add_course'],
            'course_number' : ['2221'],
            'name' : ['Software 1: Software Components']
        }

        # Track number of courses in DB before POST
        num_courses_before = Course.objects.all().count()

        # Make POST
        response = self.client.post(ADMIN_FORM_URL, data=course_data, follow=True)

        self.assertTrue(response.context['course_form'].is_valid())

        # Assert the number of courses in the DB increased by 1
        num_courses_after = Course.objects.all().count()
        self.assertEqual(num_courses_after, num_courses_before + 1)

        # Validate the course object is created as intended
        course = Course.objects.get(course_number='2221')

        self.assertEqual(course.course_number, '2221')
        self.assertEqual(course.name, 'Software 1: Software Components')

    def test_edit_course_modifies_course(self):

        # Add Course to the database
        new_course = Course(course_number='2221', name='Name to be changed')
        new_course.save()

        # Make POST request to update the course name
        course_data = {
            'update_course' : ['update_course'],
            'course_number' : ['2221'],
            'name' : ['Software 1: Software Components']
        }
        response = self.client.post(ADMIN_FORM_URL, data=course_data, follow=True)

        # Verify the course name was changed
        self.assertTrue(response.context['course_form'].is_valid())        
        course = Course.objects.get(course_number='2221')

        self.assertEqual(course.course_number, '2221')
        self.assertNotEqual(course.name, 'Name to be changed')
        self.assertEqual(course.name, 'Software 1: Software Components')

    def test_delete_course_removes_course(self):

        # Add Course to the database
        new_course = Course(course_number='2221', name='Software 1: Software Components')
        new_course.save()

        # Make POST request to delete the course
        course_data = {
            'delete_course' : ['delete_course'],
            'course_number' : ['2221'],
        }

        self.client.post(ADMIN_FORM_URL, data=course_data, follow=True)

        # Verify the course was deleted
        course = Course.objects.filter(course_number='2221')
        self.assertFalse(course.exists())
