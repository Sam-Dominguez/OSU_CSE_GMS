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

prevclasses = ['2221','2222','2421','2432','3521','3461','3231','3232','99999','0000','9','22']
def algoTest(request):
    cleanTestCase= True
    # cleanData = False
    # if cleanData:
    # DO NOT CALL clearDB(), DELETE YOUR DB FILE
    #     clearDB()
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

    # get all courses and sort in descending order so 5911 gets assigned first 
    courses = Course.objects.annotate(course_number_int=Cast('course_number', IntegerField()))
    courses = courses.order_by('-course_number_int')
    # loop through all sections and make assignments
    for cour in courses:
        
        # get all unassigned students that meet the requirements for 
        # valid graders. In columbus = 1
        validUnassign = UnassignedStudent.objects.filter(student_id__in_columbus = 1 ).values('student_id')
        # get all PrevClassTaken which relate to students unassigned and is for the current course
        validStudents = PreviousClassTaken.objects.filter(course_number = cour.course_number, student_id__in=validUnassign)
        # get all sections that need graders to assign for
        sections = Section.objects.filter(course_number = cour.course_number, num_graders_needed__gt = 0,semester = assignSemester )

        for sect in sections:
            if validStudents:
                selectFromPriority(sect,validStudents)
            

# select students to assign for a section
def SelectStuFromSection(sec, stu ):
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
                us.delete()
                sec.num_graders_needed -= 1
        else:
            break
    return sec, stu
    

# Considers priority and instructor preferences
def selectFromPref(section, pClassTaken):
    for i in range(3):
        curPrio = pClassTaken.filter(pref_num = i) # only check for this prio

        # get all students in current priority that stated they wanted the instructor
        wantInstruct = curPrio.filter(instructor= section.instructor)
        section,wantInstruct = SelectStuFromSection(section,wantInstruct)

        if section.num_graders_needed > 0: # section not filled, go to lower prio
            # select with no instructor pref, so can just select because instructor is end of priority
            section, curPrio = SelectStuFromSection(section,curPrio) 
    return section, pClassTaken
        
# selects students for one section based on priority.
def selectFromPriority(section, pClassTaken):
    prevGrader = pClassTaken.filter(student_id__previous_grader  = 1)
    gradedLastTerm = prevGrader.exclude(student_id__graded_last_term__exact='')

    # select with full priority path
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
        


















