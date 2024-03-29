from django.template.defaulttags import register
from OSU_CSE_GMS.models import Course
from ..services import permissions

@register.filter
def get_total_graders_needed(course_number):
    try:
        course = Course.objects.get(course_number=course_number)
        total_graders_needed = sum(section.num_graders_needed for section in course.section_set.all())
    except Course.DoesNotExist:
        total_graders_needed = 0
    return total_graders_needed

@register.filter(name='has_group') 
def has_group(user, group_name):
    return permissions.has_group(user, group_name)