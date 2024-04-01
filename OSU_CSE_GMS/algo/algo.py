from ..models import *
from ..services import email_service
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
from typing import Tuple 
from django.db.models.query import QuerySet
LOGGER = logging.getLogger('django')

# run to clear db, parse csv data to database, and then run massAssign to make assignments.
def algoTest(request):
    #if true, attempts to parse the csv data to fill the database. After parsing, 
    #create fixtures with it because parsing and loading is very slow.
    cleanTestCase= False
    #Deleting everything in database, might be better to delete your db file.
    cleanData = False
    if cleanData:
        clearDB()
    if cleanTestCase:
        curDir = os.path.abspath(os.path.dirname(__file__))
        loadCourses( os.path.join(curDir,'csv_data/all_courses.csv')) # parse all Courses
        loadInstructors(os.path.join(curDir,'csv_data/all_course_instructor.csv')) # gets instructors and creates sections
        loadStudentInput(os.path.join(curDir,'csv_data/grader_input_data.csv'))# load all the students and their input data.
    context = {

    }
    massAssign(assignSemester="SP2024") # make assignments 
    return render(request, 'algo.html', context) # algo.html is empty, this is just used to run code.

    
"""
massAssign is the function to call to make assignments in batches. 
It will get all courses and order them with highest numbered courses to be assigned first.
It will go through the sections for a course twice. The first time is to honor instructor 
preferences. This is because people who put instructors have a higher priority, so look at them first.
The second pass through the sections will include everybody, it will also go to the the database to 
query the PreviousClass takens and sections again. This is due to the fact that querys are fast (Although
when making the final assignment, it checks for a existing assignment already so not actually neccessary) and 
it is expected that a good amount of students will be taken after going through every section. 
Note that there is loop through every section in a course, for the first section loop, it will only get the 
Previous Class taken with a matching instructor for that section. Also note it is matching with instructor EMAIL.
The second section loop just gets all viable students which is basically not caring about whether a student
has a instructor preference or not.

One important WARNING about this is that course number has HIGHEST priority. This means even if a student has graded
last term and puts their 1st preference for that class with instructor preference for a 4XXX, if there 2nd or third preference
which has a class like a higher number 5524, massAssign will put them in 5524. This was not a communicated preference from sponsor.
But given there is difficulty in getting graders for higher number courses, this is a decision made to simplify things. An easy
way to get rid of this problem is perhaps getting all graders who have put preferences/graded before and running them all throught it
like with two passes to handle instructor preferences. Too many loops is rather problamatic so getting all preferences and 
going through them(students) one by one after randomizing the list might also be a good solution, but this is all a big IF. 
"""
# Runs algroithm to assign in mass, semeseter is AU,SP,SU + XXXX
def massAssign(assignSemester: str) -> None:
    LOGGER.info("~~BEGINNING MASS ASSIGN~~")
    # get all courses and sort in descending order so a higher number 5911 gets assigned first, 1111 would be near last
    courses = Course.objects.annotate(course_number_int=Cast('course_number', IntegerField()))
    courses = courses.order_by('-course_number_int')
    # loop through all sections and make assignments
    for cour in courses:
        # get students and sections for this course. Students are valid and unassigned. Sections need graders.
        validStudents,sections = retrievePrevClassAndSections(cour,assignSemester)
        instructorsForSections = sections.values_list('instructor__email', flat=True).distinct()
        # instructor preferences have a higher priority, so only look at people that put an instructor
        # Look for students who have a instructor preference in any of the sections first. 
        validStudentsInstructPref: QuerySet[PreviousClassTaken] = validStudents.filter(instructor__in = instructorsForSections)
        if validStudentsInstructPref:
            for sect in sections:
                # get all PrevClassTaken with matching instructor for this section
                curSectInstructPref = validStudentsInstructPref.filter(instructor = sect.instructor.email)
                if curSectInstructPref:
                    select_based_on_priority(sect,curSectInstructPref,cour)
        # now that all instructor preferences are taken care of, can disregard instructor preferences
        #  Basically everyone that has a matching course number in previousClassTaken
        # we filter again because sections could have been changed in previous run.
        validStudents, sections = retrievePrevClassAndSections(cour,assignSemester)
        if validStudents:
            for sect in sections:
                select_based_on_priority(sect,validStudents,cour)
            
    LOGGER.info("~~ENDING MASS ASSIGN~~")
    email_service.notify_assignments_complete()

"""
This will get the valid students and sections that could be assigned to a course.
Valid students is right now just 'in columbus = 1 (true) and if they are also unassigned'.
Students from now on will be represented only be PreviousClassTaken. So each student can have 
a max of 3 representations of PreviousClassTaken.
Sections are sections of a Course and only pulled if they need graders and also of the same Semeser.
"""
# gets valid unassigned student's PreviousClassTaken and Sections that need graders for a course that needs to be assigned
def retrievePrevClassAndSections(cour: Course,assignSemester: str)-> Tuple[QuerySet[PreviousClassTaken], QuerySet[Section]]:
         # get all unassigned students that meet the requirements for 
        # valid graders. In columbus = 1
        validUnassign = UnassignedStudent.objects.filter(student_id__in_columbus = 1 ).values_list('student_id',flat=True)
        # get all PrevClassTaken which relate to students unassigned and is for the current course
        validStudents= PreviousClassTaken.objects.filter(course_number = cour, student_id__in=validUnassign)
        # get all sections that need graders to assign for
        sections = Section.objects.filter(course_number = cour, num_graders_needed__gt = 0,semester = assignSemester )
        return validStudents, sections

"""
This is where the actual Assignment gets created. The students are randomized at start to ensure there is no time priority
or any other kind of unfair advantage. Want to ensure if they all meet the deadline, they have equal chances.
This will check again if the student is unassigned and to check assignments to prevent unique together error.
unique_together = [['student_id', 'course_number']]. This is needed because remember that only the querysets
from massAssign function are Query from the database. The rest are modifying a queryset in memory, so there will
be duplicate students that have already been assigned so there is an absolute need to check or the system will crash.
Also see how the section is MODIFIED, but it is the one in memory. NOT the one in the database. The section is saved
last once it has went through all the priorities, there is many sec.num_graders_needed>0  to reach the end quickly .
"""
# select students to assign for a section
def create_assignments_for_section(sec:Section, stu:QuerySet[PreviousClassTaken] ) -> Tuple[Section,QuerySet[PreviousClassTaken]]:
    # randomize students to ensure that all students who met deadline have a fair chance.
    randomStu = stu.order_by(Random())
    for s in randomStu:
        # only make assignments for a section that needs graders
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
                    email_service.notify_single_assignment(a)
                status_code = us.delete()[0]
                if status_code == 0:
                    LOGGER.error(f'Failed to delete unassigned student with student id: {s.student_id.id}')
                else:
                    LOGGER.info(f'Successfully deleted unassigned student with student id: {s.student_id.id}')
                sec.num_graders_needed -= 1
        else:
            break
    return sec, stu
    
# Considers priority of preferences (1,2,3) with 1 being highest so look at it first. 
# At a high level, looks at all students who put the section as their first preference first.
def consider_preference_priority(section: Section, pClassTaken: QuerySet[PreviousClassTaken]) -> Tuple[Section,QuerySet[PreviousClassTaken]]:
    for i in range(1,4): # priority is 1,2, or 3.
        curPrio: QuerySet[PreviousClassTaken] = pClassTaken.filter(pref_num = i) # only check for this preference priority.
        section,curPrio = create_assignments_for_section(section,curPrio)
    return section, pClassTaken

"""
This will go through all the main prioritys the algorithm will consider. It will start by looking 
at the highest priority first. It will incrementally build a queryset with higher priority and thus also
a smaller one. If highest priority fails, then it will fall back on the querysets that were already built
to reach the highest priority to do further processing if needed. The pClass takens is just all valid students,
it is not used in searching because the first filter looks at Previous graders, so the last thing to look at is
the opposite which is not previous graders, so there is no need to look at all of pClassTaken for the final search 
because all Previous graders graders are guareenteed to fail.

The second priority increase is if a student has graded last term. The second filter, is an EXCLUDE, this means students 
who put nothing in graded last term will have a lower priority.
There is a worry that putting something random there will give them priority.This is something that is better addressed
during intake so there is something random in the database.

The third and final priority increase is if they have graded the same course last semester. 
Then it will start considering looking at all students who put the class as their first preference 
with the function consider_preference_priority().

After the highest priority fails, it falls back to the second priority increase queryset
After that fails, it will fall back to look at previous graders that did not grade last term by doing a filter
with the first queryset(previous grader) to get the opposite of the second priority increase queryset. Notice the use 
filter instead of exclude with the same parameters to get the rest of PreviousClassTaken not already looked at.
After that fails, as said in the first paragrash it will look at new graders, which is the
opposite of all previous graders so use the given query set in parameters filter with.

See how it SAVES the SECTION to the database at the very END after trying to assign for the section. This what
the returns of Section, QuerySet[PreviousClassTaken] are for. The QuerySet[PreviousClassTaken] not used as it is
not modified. Do not think that you just remove a student from the queryset in a deeper function because the
returns of QuerySet[PreviousClassTaken] are NEVER used so removing a student is useless. This is because there is a
preference to not build the querysets over again. The Section on the other hand might change its section.num_graders_needed changed.
"""
# selects students for one section based on priority.
def select_based_on_priority(section: Section, pClassTaken : QuerySet[PreviousClassTaken] ,course: Course):
    prevGrader = pClassTaken.filter(student_id__previous_grader  = 1) # previous graders
    gradedLastTerm = prevGrader.exclude(student_id__graded_last_term__exact='') # graded last term
    gradedLastTermSameCourse = gradedLastTerm.filter(student_id__graded_last_term = course.course_number) # graded last term, same course
    
    # select with full priority path
    section,gradedLastTermSameCourse = consider_preference_priority(section,gradedLastTermSameCourse)
    if section.num_graders_needed > 0: # section not filled, go to lower prio
        # graded last term for the same course failed, look at all who graded Last term
        section,gradedLastTerm = consider_preference_priority(section,gradedLastTerm)
    if section.num_graders_needed > 0: # section not filled, go to lower prio
        # gradedLastTerm failed, so look at not graded last term
        notGradedLastTerm = prevGrader.filter(student_id__graded_last_term__exact='')
        section,notGradedLastTerm = consider_preference_priority(section,notGradedLastTerm)
    if section.num_graders_needed > 0: # section not filled, go to lower prio
        # all Previous grader failed, so look at not graders. Lowest Priority
        notPrevGrader = pClassTaken.filter(student_id__previous_grader = 0)
        section,notPrevGrader = consider_preference_priority(section,notPrevGrader)
    # done with this section, save it. Updating the num_graders_needed field
    section.save()


# Not exact, just the thought process of the whole algorithm.
# get only in columbus
# loop through courses
#   loop through sections
        # if prevGrader:
        #     if gradedLastTerm:
        #         if gradedSameCourse
        #             if run through pref(1,2,3). :
        #                 checkInstructors (instructors is actually checked before loop through sections)
        #             else:
        #                 noInstructors
        #         else:
        #             not graded same Course
        #     else:
        #         prevgrader
        # else:
        #     notPrevGrader
        

