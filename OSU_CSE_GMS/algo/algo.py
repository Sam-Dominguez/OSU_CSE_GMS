from ..models import *
from django.shortcuts import render
import random
from django.db.models.functions import Random
from django.db.models import Q
from .load_csv_db import *
from django.db.models import IntegerField
from django.db.models.functions import Cast
import os
import os.path
import logging

LOGGER = logging.getLogger('django')

prevclasses = ['2221','2222','2421','2432','3521','3461','3231','3232','99999','0000','9','22']
def algoTest(request):
    cleanTestCase= False
    cleanData = False
    if cleanData:
        clearDB()
    
    if cleanTestCase:
        curDir = os.path.abspath(os.path.dirname(__file__))
        loadCourses( os.path.join(curDir,'csv_data/all_courses.csv'))
        loadInstructors(os.path.join(curDir,'csv_data/all_course_instructor.csv'))
        loadStudentInput(os.path.join(curDir,'csv_data/grader_input_data.csv'))
 
    # random testing
    context = {

    }
    
    massAssign("SP2024")
    return render(request, 'algo.html', context)
    

# algorithm to assign graders in mass/batches
def massAssign(assignSemester):

    LOGGER.info("~~BEGINNING MASS ASSIGN~~")

    # get all courses and sort in descending order so 5911 gets assigned first 
    courses = Course.objects.annotate(course_number_int=Cast('course_number', IntegerField()))
    courses = courses.order_by('-course_number_int')
    # loop through all sections and make assignments
    for cour in courses:
        # get students and sections for this course. Students are valid unassigned. Sections need graders
        validStudents, sections = retrievePrevClassAndSections(cour,assignSemester)

        instructorsForSections = sections.values_list('instructor__email', flat=True).distinct()
        # instructor preferences have a higher priority, so only look at people that put an instructor
        # preference which is also a instructor in any of the sections first. 
        validStudentsInstructPref = validStudents.filter(instructor__in = instructorsForSections)
        if validStudentsInstructPref:
            for sect in sections:
                # get all PrevClassTaken with matching instructor for this section
                curSectInstructPref = validStudentsInstructPref.filter(instructor = sect.instructor.email)
                if curSectInstructPref:
                    selectFromPriority(sect,curSectInstructPref,cour.course_number)
        
        # now that all instructor preferences are taken care of, can disregard instructor preferences
        #  Basically everyone that has a matching course number in previousClassTaken
        # we filter again because sections could have been changed in previous run.
        validStudents, sections = retrievePrevClassAndSections(cour,assignSemester)
        if validStudents:
            for sect in sections:
                selectFromPriority(sect,validStudents,cour.course_number)
            
    LOGGER.info("~~ENDING MASS ASSIGN~~")

# gets PreviousClassTaken and sections for a course that needs to be assigned
def retrievePrevClassAndSections(cour,assignSemester):
         # get all unassigned students that meet the requirements for 
        # valid graders. In columbus = 1
        validUnassign = UnassignedStudent.objects.filter(student_id__in_columbus = 1 ).values_list('student_id',flat=True)
        # get all PrevClassTaken which relate to students unassigned and is for the current course
        validStudents = PreviousClassTaken.objects.filter(course_number = cour.course_number, student_id__in=validUnassign)
        # get all sections that need graders to assign for
        sections = Section.objects.filter(course_number = cour.course_number, num_graders_needed__gt = 0,semester = assignSemester )
        return validStudents , sections

# select students to assign for a section
def SelectStuFromSection(sec, stu ):
    # randomize students to ensure that all students who met deadline have a fair chance.
    randomStu = stu.order_by(Random())
    for s in randomStu:
        # only make assignments for sections that need graders
        if sec.num_graders_needed > 0:
            # check if student still needs assignment.
            us = UnassignedStudent.objects.filter(student_id = s.student_id).first()
            assigned = Assignment.objects.filter(student_id = s.student_id, section_number = sec.section_number).first()
            if  us and not assigned:
                a = Assignment(student_id = s.student_id, section_number = sec, status = 'PENDING')
                a.save()

                if not a.pk:
                    LOGGER.error(f"Failed to create assignment with student id: {s.student_id.id} and section_number {sec.id}")
                else:
                    LOGGER.info(f"Created assignment with id: {a.pk} - Assigned Student Id: {s.student_id.id} to section_number id: {sec.id}")

                status_code = us.delete()[0]
                if status_code == 0:
                    LOGGER.error(f'Failed to delete unassigned student with student id: {s.student_id.id}')
                else:
                    LOGGER.info(f'Successfully deleted unassigned student with student id: {s.student_id.id}')

                sec.num_graders_needed -= 1
        else:
            break
    return sec, stu
    

# Considers priority of preferences
def selectFromPref(section, pClassTaken):
    for i in range(3):
        curPrio = pClassTaken.filter(pref_num = i) # only check for this prio
        section,curPrio = SelectStuFromSection(section,curPrio)

    return section, pClassTaken
        
# selects students for one section based on priority.
def selectFromPriority(section, pClassTaken,courseNum):
    prevGrader = pClassTaken.filter(student_id__previous_grader  = 1)
    gradedLastTerm = prevGrader.exclude(student_id__graded_last_term__exact='')
    gradedLastTermSameCourse = gradedLastTerm.filter(student_id__graded_last_term = courseNum)
    
    # select with full priority path
    section,gradedLastTermSameCourse = selectFromPref(section,gradedLastTermSameCourse)

    if section.num_graders_needed > 0: # section not filled, go to lower prio
        # graded last term for the same course failed, look at all who graded Last term
        section,gradedLastTerm = selectFromPref(section,gradedLastTerm)

    if section.num_graders_needed > 0: # section not filled, go to lower prio
        # gradedLastTerm failed, so look at not graded last term
        notGradedLastTerm = prevGrader.filter(student_id__graded_last_term__exact='')
        section,notGradedLastTerm = selectFromPref(section,notGradedLastTerm)

    if section.num_graders_needed > 0: # section not filled, go to lower prio
        # all Previous grader failed, so look at not graders. Lowest Priority
        notPrevGrader = pClassTaken.filter(student_id__previous_grader = 0)
        section,notPrevGrader = selectFromPref(section,notPrevGrader)
    
    # done with this section, save it. Updating the num_graders_needed field
    section.save()


# def selectFrompriority():
# not exact, just the thought process.
# get only in columbus
# loop through courses
# loop through sections
#     if prevGrader:
#         if gradedLastTerm:
#             if gradedSameCourse
#                 if run through pref(1,2,3). :
#                     checkInstructors
#                 else:
#                     noInstructors
#             else:
#                 not graded same Course
#         else:
#             prevgrader
#     else:
#         notPrevGrader
        


















