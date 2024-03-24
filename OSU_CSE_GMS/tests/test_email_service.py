from django.conf import settings
from django.core import mail
from django.test import TestCase
from ..services import email_service

class EmailServiceTests(TestCase):

    def test_notify_assignments_complete_sends_email(self):
        email_service.notify_assignments_complete()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Batch Assign Complete")

    def test_append_email_domain_no_domain_needed_not_student(self):

        email = "lastname.101@osu.edu"
        
        result = email_service.append_email_domain(email, is_student=False)

        self.assertEqual(email, result)

    def test_append_email_domain_no_domain_needed_is_student(self):

        email = "lastname.101@buckeyemail.osu.edu"
        
        result = email_service.append_email_domain(email, is_student=True)

        self.assertEqual(email, result)

    def test_append_email_domain_domain_needed_not_student(self):

        email = "lastname.101"
        
        result = email_service.append_email_domain(email, is_student=False)

        self.assertEqual(email + "@osu.edu", result)

    def test_append_email_domain_domain_needed_is_student(self):

        email = "lastname.101"
        
        result = email_service.append_email_domain(email, is_student=True)

        self.assertEqual(email + "@buckeyemail.osu.edu", result)