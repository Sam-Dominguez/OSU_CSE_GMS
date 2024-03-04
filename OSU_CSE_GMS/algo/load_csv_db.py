import csv
from ..models import *
# load all courses from csv with columns (Courses, Course Title)
def clearDB():
    # WARNING: CAN'T DELETE USERS or instructors. DONT CALL THIS FUNC!!

    Section.objects.all().delete()
    #Instructor.objects.all().delete()
    #User.objects.all().delete()
    Student.objects.all().delete()
    UnassignedStudent.objects.all().delete()
    Course.objects.all().delete()
    Assignment.objects.all().delete()
    PreviousClassTaken.objects.all().delete()

def loadCourses(filePath):
    with open(filePath, 'r') as file:
        reader = csv.DictReader(file)
        for r in reader:
            courseNum = r['Courses']
            created = Course.objects.filter(course_number = courseNum).first()
            if not created:
                c = Course.objects.create(
                    course_number= courseNum,
                    name = r['Course Title '] 
                )
                c.save()
    #printCourses()

#  load all instructors from csv with columns (Course, Instructor Name, Instructor email ID)
def loadInstructors(filePath):
    # map of courses which has a list of random auto created sections, prevent duplicate generated sections
    Course_sections = {}
    Section.objects.all().delete()
    with open(filePath, 'r') as file:
        reader = csv.DictReader(file)
        for r in reader:
            mCourse = r['Course']
            mEmail = r['Instructor email ID']
            mName = r['Instructor Name']
            i = Instructor.objects.filter(email = mEmail).first()
            
            # create new instructor  if not present
            # csv file data is messed up so 

            if not i: 
                u = User.objects.create_user(username=mName, email=mEmail, password='password123')
                u.save()
                newI = Instructor.objects.create(user = u, email = mEmail ,last_name = mName)
                
                newI.save()


            instr = Instructor.objects.filter(email = mEmail).first()
            c = Course.objects.filter(course_number = mCourse).first()
            s = Section.objects.filter(course_number = c, instructor = instr).first()
            # create new section if instructor does not already have a section. 
            # WARNING: this will only create one section for an instructor, but that is because the CSV file
            # has too many rows to make sense of it 
            if c and not s:
                    if c not in Course_sections:
                        Course_sections[c] = [] # create empty list of sections
                        Course_sections[c].append(0)
                    # make a new unique section
                    last_sec = Course_sections[c][len(Course_sections[c])-1]
                    sec_number = last_sec +1
                    Course_sections[c].append(sec_number)
                    # create new section
                    newS = Section.objects.create(course_number = c, section_number = str(sec_number), semester = "SP2024",
                                           instructor = instr, instruction_mode = 'SYNCHRNONOUS' , num_graders_needed = 2)
                    newS.save()
        #printInstruct()
        #printSections()

# loads student input csv
# with columns: First,Last,EmailID,Location,PrevGrader,PrevGradeCourses,Course Pref,
#Lab day/time,Yes/No Instructor Pref,Instructor Pref1,Instructor Pref2,Instructor Pref3
def loadStudentInput(filePath):
    with open(filePath, 'r') as file:
        reader = csv.DictReader(file)
        for r in reader:
            fN = r['First']
            lN = r['Last']
            em = r['EmailID']
            loc = r['Location']
            pGrader = r['PrevGrader']
            pCourses = r['PrevGradeCourses'] # if something exists, graded_last_term = true
            cPref = r['Course Pref'] # will take only 3
            p1 = r['Instructor Pref1']
            p2 = r['Instructor Pref2']
            p3 = r['Instructor Pref3']
            
            loc,pGrader,pCourses,cPref,p1,p2,p3 = parseStuInp(loc,pGrader,pCourses,cPref,p1,p2,p3)
            lId = (lN+"."+ em)
            stExist = User.objects.filter(username = lId).first()
            if not stExist:
                u = User.objects.create_user(username=lId, email=lId, password='password123')
                s = Student.objects.create(user = u,email=lId,first_name = fN,last_name = lN, in_columbus = loc,
                    previous_grader = pGrader, graded_last_term = pCourses )
                us = UnassignedStudent.objects.create(student_id = s)
                # check for course preferences
                courses = Course.objects.all()

                pref1 = courses.filter( course_number = cPref[0]).first()
                if pref1:
                    newp1 = PreviousClassTaken.objects.create(student_id = s, course_number = pref1, instructor = p1,
                                                      pref_num=1)
                    

                pref2 = courses.filter( course_number = cPref[1]).first()
                if pref2:
                    newp2 = PreviousClassTaken.objects.create(student_id = s, course_number = pref2, instructor = p2,
                                                      pref_num=2)
                   

                pref3 = courses.filter( course_number = cPref[2]).first()
                if pref3:
                    newp3 = PreviousClassTaken.objects.create(student_id = s, course_number = pref3, instructor = p3,
                                                      pref_num=3)
                            
                

    #printCourses()

# parse student input to data DB can use
def parseStuInp(loc,pGrader,pCourses,cPref,p1,p2,p3):
    if "Columbus,OH" == loc.replace(" ",""):
        loc = 1
    else:
        loc = 0
    if "Yes" == pGrader.replace(" ",""):
        pGrader = 1
    else:
        pGrader = 0
    if len(pCourses) != 0:
        pCourses = pCourses.split()
        pCourses = pCourses[0].replace(" ","")

    cPref = cPref.split(',')
    for x in range(len(cPref)):
        cPref[x] = cPref[x].replace(" ","")
    for i in range(3):
        cPref.append("") # make sure there is array length is 3
    p1 = p1.split()    
    if p1:
        p1 = p1[0]
    else:
        p1 = ''

    p2 = p2.split()   
    if p2:
        p2 = p2[0]   
    else:
        p2 = ''    

    p3 = p3.split()
    if p3:
        p3 = p3[0]
    else:
        p3 = ''
    return loc,pGrader,pCourses,cPref,p1,p2,p3

# prints all courses in db
def printCourses():
    courses = Course.objects.all()
    for c in courses:
        print(c.__dict__)

# prints all instructors in db
def printInstruct():
    instruct = Instructor.objects.all()
    for i in instruct:
        print(i.__dict__)
# prints all Sections in db
def printSections():
    sect = Section.objects.all()
    for s in sect:
        print(s.__dict__)           
            
            

                        




