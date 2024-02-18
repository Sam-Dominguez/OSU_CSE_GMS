from .models import *
from django.shortcuts import render
import random
from django.db.models.functions import Random
from django.db.models import Q
prevclasses = ['2221','2222','2421','2432','3521','3461','3231','3232','99999','0000','9','22']
def algoTest(request):
    cleanTestCase= False
    if cleanTestCase:
        addTestStudent()

    context = {}
    s = Student.objects.all()
    us = UnassignedStudent.objects.all() 

    context = {
        "students" : s,
        "unassign" : us,
        "courses" : Course.objects.all(),
        "query" : getValidStudents() 
    }
    
    getStudentsForCourses(context['query'])
    
    return render(request, 'algo.html', context)
    

# get all that are in unassigned and in columbus
def getValidStudents():
    
    unassign = UnassignedStudent.objects.filter(student_id__in_columbus = 1 )
    # for u in unassign:
    #     print(u.student_id.__dict__)
    return unassign

# given valid Unassigned students, try to find matching courses
def getStudentsForCourses(unassign):
    courses = Course.objects.all()
    print(" ")
    for c in courses:
        matches = CourseInPrevClass(unassign,c.course_number)
        if matches:
            print("valid students for CSE " + c.course_number + " : ")

            # get graded before and new grader priority
            gradedBefore = matches.filter(student_id__previous_grader = 1).order_by(Random())
            newGrader = matches.filter(~Q(student_id__previous_grader = 1)).order_by(Random())

            print("graded before:")
            for m in gradedBefore:
                print(m.student_id.__dict__)

            print("\nNot graded before:")
            for m in newGrader:
                print(m.student_id.__dict__)
        else:
            print("No valid students for CSE " + c.course_number)
        print(" ")
    
# given unassigned students query set and a course number (string), find all unassigned Students that match with course
def CourseInPrevClass(unassign, course):
    
    # Check if any UnassignedStudent has the course_number in previous_classes
    matchList = [
        student.pk
        for student in unassign
        if any(course == c for c in student.student_id.previous_classes.split())
    ]
    matches= unassign.filter(pk__in=matchList)

    return matches
    
# deletes all current courses and makes 10 dummy courses
def makeCourses():
    Course.objects.all().delete()
    for i in range(0,12):
        c = Course(course_number= prevclasses[i],name ="CSE: " + str(i) )
        c.save()

# deletes all students and unassigned. Then adds students and also adds them to be unassigned
def addTestStudent():
    User.objects.exclude(is_superuser=True).delete()
    Student.objects.all().delete()
    UnassignedStudent.objects.all().delete()
    for i in range(10):
        user1 = User.objects.create_user(username=str(i), email=str(i)+"@mail.com", password='password123')
        user2 = User.objects.create_user(username=str(i+10), email=str(i)+"@mail.com", password='password123')
        user3 = User.objects.create_user(username=str(i+20), email=str(i)+"@mail.com", password='password123')
        user1.save()
        user2.save()
        user3.save()

        #1
        t = Student(id= i,user = user1,email=str(i)+'@.com',first_name = str(i),last_name = str(i), in_columbus = i%2,
                    previous_grader = (i+1)%2,previous_classes = prevclasses[i]+ " " + prevclasses[random.randrange(10)]
                    + " " + prevclasses[random.randrange(10)])
        t.save()
        u=UnassignedStudent(student_id =t)
        u.save()

        #2
        s = Student(id= (i+10),user = user2,email=str(i)+'@.com',first_name = str(i),last_name = str(i), in_columbus = (i+1)%2,
                    previous_grader = (i%2),previous_classes = prevclasses[i]+ " " + prevclasses[random.randrange(10)]
                    + " " + prevclasses[random.randrange(10)])
        s.save()
        r=UnassignedStudent(student_id =s)
        r.save()

        #3
        n = Student(id= (i+20),user = user3,email=str(i)+'@.com',first_name = str(i),last_name = str(i), in_columbus = i%2,
                    previous_grader = (i%2),previous_classes = prevclasses[i]+ " " + prevclasses[random.randrange(10)]
                    + " " + prevclasses[random.randrange(10)])
        n.save()
        m=UnassignedStudent(student_id =n)
        m.save()
   
    