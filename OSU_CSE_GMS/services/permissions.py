from django.contrib.auth.models import User

STUDENT_GROUP = "students"
ADMINISTRATOR_GROUP = "administrators"
INSTRUCTOR_GROUP = "instructors"

def has_group(user: User, group_name: str):
    '''
    True if a user has group named group_name, false otherwise. Superusers will always return true.
    '''
    return user.is_superuser or user.groups.filter(name=group_name).exists()