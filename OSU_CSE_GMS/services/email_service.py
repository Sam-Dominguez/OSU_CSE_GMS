import logging
from django.core import mail
from django.core.mail import EmailMessage
from ..models import Assignment, Section

LOGGER = logging.getLogger('django')

FROM_EMAIL = "test@testing.com" # TODO: change to appropriate from email
ADMIN_EMAIL = "admin@osu.edu"  # TODO: change to appropriate admin monitored email

def notify_assignments_complete():
    '''
    Sends an email to the ADMIN_EMAIL notifying them that a batch of graders has been assigned.
    '''
    LOGGER.info(f'Sending email to admin')
    mail.get_connection(fail_silently=False).send_messages([EmailMessage(
        "Batch Assign Complete",
        "A new batch of graders have been assigned. Log into the OSU CSE GMS to view.",
        FROM_EMAIL,
        [ADMIN_EMAIL],
    )])

def notify_single_assignment(assignment : Assignment):
    '''
    Sends an email to the student and to the intructor of the section to which the student was assigned as a grader for.
    '''

    # Get section of assignment
    section_number = assignment.section_number

    section_object = Section.objects.filter(id=section_number.pk)

    section = section_object[0] if section_object.exists() else None

    if section is None:
        LOGGER.error(f'Could not find section with id {section_number}. Cannot notify instructor.')
        return
    
    # Get instructor email
    instructor_email = section.instructor.email
    instructor_email = append_email_domain(instructor_email, is_student=False)

    if not instructor_email:
        LOGGER.info("Did not find instructor email")
        return

    # Get student email
    student_email = assignment.student_id.email
    student_email = append_email_domain(student_email, is_student=True)

    if not student_email:
        LOGGER.info("Did not find student email")
        return
    
    # Email to instructor
    email_instructor = EmailMessage(
        "You have a new grader",
        f'Your {section.course_number} Section {section.section_number} has been assigned a grader: {assignment.student_id.first_name} {assignment.student_id.last_name} ({student_email}).',
        FROM_EMAIL,
        [instructor_email],
    )

    # Email to student
    email_student = EmailMessage(
        "You have a new grader assignment",
        f'You have been assigned {section.course_number}, Section {section.section_number} with {section.instructor}, ({instructor_email}). Log into the OSU CSE GMS to view!',
        FROM_EMAIL,
        [student_email],
    )

    # Send emails
    LOGGER.info(f'Sending emails to instructor: {instructor_email} and student {student_email}')
    mail.get_connection(fail_silently=False).send_messages([email_instructor, email_student])


def append_email_domain(email: str, is_student: bool):
    '''
    If necessary, appends the appropriate email domain if the email is for a student (@buckeyemail.osu.edu) or instructor (@osu.edu)
    '''
    if email.find("@") != -1:
        LOGGER.info(f'Email {email} has a domain, no appending needed')
        return email
    
    if is_student:
        return email + "@buckeyemail.osu.edu"
    else:
        return email + "@osu.edu"
