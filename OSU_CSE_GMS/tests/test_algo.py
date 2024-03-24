from django.core import mail
from django.test import TestCase
from OSU_CSE_GMS.models import *
from ..algo.algo import massAssign
import inspect
import os
import os.path


#WARNING all sections 2321 and 3341 have been edited in some testcase to have a different number of graders need.Take caution.

class AdministratorTests(TestCase):
    curDir = os.path.abspath(os.path.dirname(__file__))
    dbPath = os.path.join(curDir,'fixtures/initial_data.json')
    fixtures = [dbPath]

    # tests instructor preference has priority over none and will properly always pick matching instructors
    def testInstructorPref(self):
        curFunc= inspect.currentframe().f_code.co_name
        
        cour3902 = Course.objects.filter(course_number = "3902").first()
        u = User.objects.create_user(username="algoUnitTest1-1", email="algoUnitTest1-1", password='password123')
        s1 = Student.objects.create(user = u,email="algoUnitTest1",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3902, instructor = "kirby.249" ,
                                                      pref_num=1)
        u = User.objects.create_user(username="algoUnitTest1-2", email="algoUnitTest1-2", password='password123')
        s2 = Student.objects.create(user = u,email="algoUnitTest1-2",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp1 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3902, instructor = "boggus.2" ,
                                                      pref_num=1)
        
        u = User.objects.create_user(username="algoUnitTest1-3", email="algoUnitTest1-3", password='password123')
        s3 = Student.objects.create(user = u,email="algoUnitTest1-3",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp1 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3902, instructor = "" ,
                                                      pref_num=1)
        
        # there should be 1 spot taken already in 3902 boguss, 2 is open in kirby before assignment
        # test 5 times to ensure it is not randomly correct because assignments are made randomly
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            instructKirby = Instructor.objects.filter(email = 'kirby.249').first()
            instructBoggus = Instructor.objects.filter(email = 'boggus.2').first()
            sections3902 = Section.objects.filter(course_number = cour3902 )
            sectionKirby = sections3902.filter(instructor = instructKirby).first()
            sectionBoggus = sections3902.filter(instructor = instructBoggus).first()
            for s in sections3902:
                self.assertEqual(s.num_graders_needed, 0)
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),3)

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email
            
            # make sure they all went to correct assignments
            s1GoToKirby = assignments.filter(student_id = s1).first()
            s2GoToBoggus = assignments.filter(student_id = s2).first()
            s3GoToKirby =assignments.filter(student_id = s3).first()
            self.assertEqual(s1GoToKirby.section_number,sectionKirby)
            self.assertEqual(s2GoToBoggus.section_number,sectionBoggus)
            self.assertEqual(s3GoToKirby.section_number,sectionKirby)
            sectionBoggus.num_graders_needed = 1
            sectionKirby.num_graders_needed = 2
            us1.save()
            us2.save()
            us3.save()
            s1GoToKirby.delete()
            s2GoToBoggus.delete()
            s3GoToKirby.delete()
            sectionBoggus.save()
            sectionKirby.save()

    # tests if no instruct pref, still gets assigned
    def testInstructorPref2(self):
        curFunc= inspect.currentframe().f_code.co_name
        
        cour3902 = Course.objects.filter(course_number = "3902").first()
        u = User.objects.create_user(username="algoUnitTest11-1", email="algoUnitTest11-1", password='password123')
        s1 = Student.objects.create(user = u,email="algoUnitTest11",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3902, instructor = "kirby.249" ,
                                                      pref_num=1)
        u = User.objects.create_user(username="algoUnitTest11-2", email="algoUnitTest11-2", password='password123')
        s2 = Student.objects.create(user = u,email="algoUnitTest11",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp1 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3902, instructor = "boggus.2" ,
                                                      pref_num=1)
        
        u = User.objects.create_user(username="algoUnitTest11-3", email="algoUnitTest11-3", password='password123')
        s3 = Student.objects.create(user = u,email="algoUnitTest11-3",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp1 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3902, instructor = "" ,
                                                      pref_num=1)
        
        for i in range(2):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            instructKirby = Instructor.objects.filter(email = 'kirby.249').first()
            instructBoggus = Instructor.objects.filter(email = 'boggus.2').first()
            sections3902 = Section.objects.filter(course_number = cour3902 )
            sectionKirby = sections3902.filter(instructor = instructKirby).first()
            sectionBoggus = sections3902.filter(instructor = instructBoggus).first()
            for s in sections3902:
                self.assertEqual(s.num_graders_needed, 0)
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),3) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            # make sure they all went to correct assignments
            a1 = assignments.filter(student_id = s1).first()
            a2 = assignments.filter(student_id = s2).first()
            a3 =assignments.filter(student_id = s3).first()
            sectionBoggus.num_graders_needed = 1
            sectionKirby.num_graders_needed = 2
            us1.save()
            us2.save()
            us3.save()
            a1.delete()
            a2.delete()
            a3.delete()
            sectionBoggus.save()
            sectionKirby.save()

    # tests if having a wrong instructor pref is equal to having same as someone with no pref. Cannot test properly, even if 
    # num of greeders needed 1 because it is mass assigned, can't tell. So make sure the next lower priority is never assigned
    def testInstructorPref3(self):
        curFunc= inspect.currentframe().f_code.co_name
        
        cour2123 = Course.objects.filter(course_number = "2123").first()
        u = User.objects.create_user(username="algoUnitTest16-1", email="algoUnitTest16-1", password='password123')
        s1 = Student.objects.create(user = u,email="algoUnitTest16",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour2123, instructor = "kirby.249" ,
                                                      pref_num=1)
        u = User.objects.create_user(username="algoUnitTest16-2", email="algoUnitTest16-2", password='password123')
        s2 = Student.objects.create(user = u,email="algoUnitTest16-2",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp1 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour2123, instructor = "" ,
                                                      pref_num=1)
        
        u = User.objects.create_user(username="algoUnitTest16-3", email="algoUnitTest16-3", password='password123')
        s3 = Student.objects.create(user = u,email="algoUnitTest16-3",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp1 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour2123, instructor = "" ,
                                                      pref_num=1)
        
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            instruct = Instructor.objects.filter(email = 'pichkar.3').first()
            section = Section.objects.filter(course_number = cour2123 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),2) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            # make sure they all went to correct assignments
            a1 = assignments.filter(student_id = s1).first()
            a2 = assignments.filter(student_id = s2).first()

            self.assertEqual(a1.section_number,section)
            self.assertEqual(a2.section_number,section)
            section.num_graders_needed = 2
            us1.save()
            us2.save()
            us3.save()
            a1.delete()
            a2.delete()
            section.save()
           
    # tests if correct instructor chosen out of 3 choices
    def testInstructorPref4(self):
        curFunc= inspect.currentframe().f_code.co_name
        
        cour3341 = Course.objects.filter(course_number = "3341").first()
        u = User.objects.create_user(username="algoUnitTest17-1", email="algoUnitTest17-1", password='password123')
        s1 = Student.objects.create(user = u,email="algoUnitTest17",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us1 = UnassignedStudent.objects.create(student_id = s1)
    
        
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3341, instructor = "shareef.1" ,
                                                      pref_num=1)
        
        instruct = Instructor.objects.filter(email = 'shareef.1').first()
        section = Section.objects.filter(course_number = cour3341 )
        
        for s in section:
            s.num_graders_needed = 2
            s.save()
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            instruct = Instructor.objects.filter(email = 'shareef.1').first()
          
            section = Section.objects.filter(course_number = cour3341)
            self.assertEqual(section.count(),3)

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            sectionShareef = section.filter(instructor = instruct).first()
            assignments = Assignment.objects.filter(student_id__in = [s1])
            self.assertEqual(assignments.count(),1) 
            # make sure they all went to correct assignments
            s1GoToShareef = assignments.filter(student_id = s1).first()
            
            self.assertEqual(s1GoToShareef.section_number,sectionShareef)

            sectionShareef.num_graders_needed = 2
            us1.save()
            s1GoToShareef.delete()
            sectionShareef.save()

    # tests if correct instructor chosen out of 5 choices
    def testInstructorPref5(self):
        curFunc= inspect.currentframe().f_code.co_name
        
        cour2321 = Course.objects.filter(course_number = "2321").first()
        u = User.objects.create_user(username="algoUnitTest18-1", email="algoUnitTest18-1", password='password123')
        s1 = Student.objects.create(user = u,email="algoUnitTest18",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = 3902)
        us1 = UnassignedStudent.objects.create(student_id = s1)
    
        
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour2321, instructor = "close.2" ,
                                                      pref_num=1)
        
        instruct = Instructor.objects.filter(email = 'close.2').first()
        section = Section.objects.filter(course_number = cour2321)
        
        for s in section:
            s.num_graders_needed = 2
            s.save()
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            instruct = Instructor.objects.filter(email = 'close.2').first()
          
            section = Section.objects.filter(course_number = cour2321)
            self.assertEqual(section.count(),5)
            sectionClose = section.filter(instructor = instruct).first()
            assignments = Assignment.objects.filter(student_id__in = [s1])

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            self.assertEqual(assignments.count(),1) 
   
            a1 = assignments.filter(student_id = s1).first()
            self.assertEqual(a1.section_number,sectionClose)
            sectionClose.num_graders_needed = 2
            us1.save()
            a1.delete()
            sectionClose.save()


    # make sure preference priority 1,2 always has priority over 3
    def testPrefPriority1(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour2123 = Course.objects.filter(course_number = "2123").first()

        u1 = User.objects.create_user(username="algoUnitTest2-1", email="algoUnitTest2-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest2",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour2123, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest2-2", email="algoUnitTest2-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest2",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour2123, instructor = "" ,
                                                      pref_num=2)
        u3 = User.objects.create_user(username="algoUnitTest2-3", email="algoUnitTest2-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest2",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us3 = UnassignedStudent.objects.create(student_id = s3)

        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour2123, instructor = "" ,
                                                      pref_num=3)

        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section2123 = Section.objects.filter(course_number = cour2123 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            self.assertEqual(assignments.count(),2) 
            s1AssignedFirst = assignments.filter(student_id = s1).first()
            self.assertEqual(s1AssignedFirst.section_number,section2123)
            s2AssignedSecond = assignments.filter(student_id = s2).first()
            self.assertEqual(s2AssignedSecond.section_number,section2123)
            section2123.num_graders_needed = 2
            us1.save()
            us2.save()
            us3.save()
            s1AssignedFirst.delete()
            s2AssignedSecond.delete()
            section2123.save()

     # make sure preference priority 1 over 2 and 3 where graded_last term is excluded
    def testPrefPriority2(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest3-1", email="algoUnitTest3-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest3",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest3-2", email="algoUnitTest3-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest3",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3232, instructor = "" ,
                                                      pref_num=2)
        u3 = User.objects.create_user(username="algoUnitTest3-3", email="algoUnitTest3-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest3",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3232, instructor = "" ,
                                                      pref_num=3)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            s1AssignedFirst = assignments.filter(student_id = s1).first()
            self.assertEqual(s1AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            us2.save()
            us3.save()
            s1AssignedFirst.delete()
            section3232.save()

    # make sure preference priority 3 will be picked 
    def testPrefPriority3(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest10-1", email="algoUnitTest10-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest10",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "2123")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=3)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            s1AssignedFirst = assignments.filter(student_id = s1).first()
            self.assertEqual(s1AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            s1AssignedFirst.delete()
            section3232.save()

    # test for graded_last_term priority if student has matching course in field graded_last_term 
    def testGradedLastTerm(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest4-1", email="algoUnitTest4-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest4",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest4-2", email="algoUnitTest4-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest4",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "3231")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3232, instructor = "" ,
                                                      pref_num=2)
        u3 = User.objects.create_user(username="algoUnitTest4-3", email="algoUnitTest4-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest4",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "3232")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3232, instructor = "" ,
                                                      pref_num=3)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            s3AssignedFirst = assignments.filter(student_id = s3).first()
            self.assertEqual(s3AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            us2.save()
            us3.save()
            s3AssignedFirst.delete()
            section3232.save()
    # test for graded_last_term priority if not matching class but just graded last term
    def testGradedLastTerm2(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest5-1", email="algoUnitTest5-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest5",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest5-2", email="algoUnitTest5-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest5",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "3231")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3232, instructor = "" ,
                                                      pref_num=2)
        u3 = User.objects.create_user(username="algoUnitTest5-3", email="algoUnitTest5-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest5",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3232, instructor = "" ,
                                                      pref_num=3)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            s2AssignedFirst = assignments.filter(student_id = s2).first()
            self.assertEqual(s2AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            us2.save()
            us3.save()
            s2AssignedFirst.delete()
            section3232.save()



    # test prevGraded priority over not graded
    def testPrevGrader(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest6-1", email="algoUnitTest6-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest6",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest6-2", email="algoUnitTest6-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest6",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3232, instructor = "" ,
                                                      pref_num=2)
        u3 = User.objects.create_user(username="algoUnitTest6-3", email="algoUnitTest6-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest6",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3232, instructor = "" ,
                                                      pref_num=3)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            s3AssignedFirst = assignments.filter(student_id = s3).first()
            self.assertEqual(s3AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            us2.save()
            us3.save()
            s3AssignedFirst.delete()
            section3232.save()

    # test prevGraded priority over not graded. all pref_num = 1
    def testPrevGrader2(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest7-1", email="algoUnitTest7-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest7",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest7-2", email="algoUnitTest7-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest6",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u3 = User.objects.create_user(username="algoUnitTest7-3", email="algoUnitTest7-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest7",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            AssignedFirst = assignments.filter(student_id = s2).first()
            self.assertEqual(AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            us2.save()
            us3.save()
            AssignedFirst.delete()
            section3232.save()

    # test prevGraded priority over not graded. with prevGraded have lowering pref num =3
    def testPrevGrader3(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest15-1", email="algoUnitTest15-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest15",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest15-2", email="algoUnitTest15-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest15",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3232, instructor = "" ,
                                                      pref_num=3)
        u3 = User.objects.create_user(username="algoUnitTest15-3", email="algoUnitTest15-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest15",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            AssignedFirst = assignments.filter(student_id = s2).first()
            self.assertEqual(AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            us2.save()
            us3.save()
            AssignedFirst.delete()
            section3232.save()


    # test not prevGraded will get assigned , if no other choice
    def testPrevGrader4(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3232 = Course.objects.filter(course_number = "3232").first()

        u1 = User.objects.create_user(username="algoUnitTest8-1", email="algoUnitTest8-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest8",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3232, instructor = "" ,
                                                      pref_num=1)

        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3232 = Section.objects.filter(course_number = cour3232 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            AssignedFirst = assignments.filter(student_id = s1).first()
            self.assertEqual(AssignedFirst.section_number,section3232)
            section3232.num_graders_needed = 1
            us1.save()
            AssignedFirst.delete()
            section3232.save()
    
    # testing if no matching courses, assignments will not be made 
    def testNoMatchToMake(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour1222 = Course.objects.filter(course_number = "1222").first()
        cour3521 = Course.objects.filter(course_number = "3521").first()
        cour4471 = Course.objects.filter(course_number = "4471").first()

        u1 = User.objects.create_user(username="algoUnitTest9-1", email="algoUnitTest9-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest9",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour1222, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest9-2", email="algoUnitTest9-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest9",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour3521, instructor = "" ,
                                                      pref_num=1)
        u3 = User.objects.create_user(username="algoUnitTest9-3", email="algoUnitTest9-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest9",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 1, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour4471, instructor = "" ,
                                                      pref_num=1)
        for i in range(2): # if it fails, it will always fail
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),0) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email


    # test if a higher number course 5236 will be assigned first, also tests if student only assigned to one open course
    def testClassNumberPriority(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3231 = Course.objects.filter(course_number = "3231").first()
        cour5236 = Course.objects.filter(course_number = "5236").first()
        cour2123 = Course.objects.filter(course_number = "2123").first()
        u1 = User.objects.create_user(username="algoUnitTest12", email="algoUnitTest12-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest12",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour2123, instructor = "" ,
                                                      pref_num=1)
    
        newp2 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3231, instructor = "" ,
                                                      pref_num=2)
       
        newp3 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour5236, instructor = "" ,
                                                      pref_num=3)
        for i in range(5):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section5236 = Section.objects.filter(course_number = cour5236 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            AssignedFirst = assignments.filter(student_id = s1).first()
            self.assertEqual(AssignedFirst.section_number,section5236)
            section5236.num_graders_needed = 2
            us1.save()
            AssignedFirst.delete()
            section5236.save()

    # test if a higher number course  assigned first, also tests if student only assigned to one open course
    def testClassNumberPriority2(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3231 = Course.objects.filter(course_number = "3231").first()
        cour2123 = Course.objects.filter(course_number = "2123").first()
        u1 = User.objects.create_user(username="algoUnitTest13-1", email="algoUnitTest13-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest13",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour2123, instructor = "" ,
                                                      pref_num=1)
    
        newp2 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3231, instructor = "" ,
                                                      pref_num=2)
       
        for i in range(3):
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section3231 = Section.objects.filter(course_number = cour3231 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            AssignedFirst = assignments.filter(student_id = s1).first()
            self.assertEqual(AssignedFirst.section_number,section3231)
            section3231.num_graders_needed = 1
            us1.save()
            AssignedFirst.delete()
            section3231.save()

    # test for people that are not in columbus to not be assigned
    def testNotInColumbus(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour3231 = Course.objects.filter(course_number = "3231").first()
        cour5236 = Course.objects.filter(course_number = "5236").first()
        cour2123 = Course.objects.filter(course_number = "2123").first()

        u1 = User.objects.create_user(username="algoUnitTest14-1", email="algoUnitTest14-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest14",first_name = curFunc ,last_name =  curFunc, in_columbus = 0,
                    previous_grader = 0, graded_last_term = "")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour3231, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest14-2", email="algoUnitTest14-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest14",first_name = curFunc ,last_name =  curFunc, in_columbus = 0,
                    previous_grader = 1, graded_last_term = "")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour2123, instructor = "" ,
                                                      pref_num=1)
        u3 = User.objects.create_user(username="algoUnitTest14-3", email="algoUnitTest14-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest7",first_name = curFunc ,last_name =  curFunc, in_columbus = 0,
                    previous_grader = 0, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour5236, instructor = "" ,
                                                      pref_num=1)
        for i in range(2):# only one run needed to show valid
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),0) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            us1.save()
            us2.save()
            us3.save()

    # test for people that are not in columbus to not be assigned. This time two others will have graded_list term but not in columbus
    # while the valid in columbus will have lower priority. Only in columbus with lower prio will get assigned
    def testNotInColumbus2(self):
        curFunc= inspect.currentframe().f_code.co_name
        cour5236 = Course.objects.filter(course_number = "5236").first()
  

        u1 = User.objects.create_user(username="algoUnitTest19-1", email="algoUnitTest19-1", password='password123')
        s1 = Student.objects.create(user = u1,email="algoUnitTest19",first_name = curFunc ,last_name =  curFunc, in_columbus = 0,
                    previous_grader = 1, graded_last_term = "5236")
        us1 = UnassignedStudent.objects.create(student_id = s1)
        newp1 = PreviousClassTaken.objects.create(student_id = s1, course_number = cour5236, instructor = "" ,
                                                      pref_num=1)
        u2 = User.objects.create_user(username="algoUnitTest19-2", email="algoUnitTest19-2", password='password123')
        s2 = Student.objects.create(user = u2,email="algoUnitTest19",first_name = curFunc ,last_name =  curFunc, in_columbus = 0,
                    previous_grader = 1, graded_last_term = "5236")
        us2 = UnassignedStudent.objects.create(student_id = s2)
        newp2 = PreviousClassTaken.objects.create(student_id = s2, course_number = cour5236, instructor = "" ,
                                                      pref_num=1)
        u3 = User.objects.create_user(username="algoUnitTest19-3", email="algoUnitTest19-3", password='password123')
        s3 = Student.objects.create(user = u3,email="algoUnitTest9",first_name = curFunc ,last_name =  curFunc, in_columbus = 1,
                    previous_grader = 0, graded_last_term = "")
        us3 = UnassignedStudent.objects.create(student_id = s3)
        newp3 = PreviousClassTaken.objects.create(student_id = s3, course_number = cour5236, instructor = "" ,
                                                      pref_num=1)
        for i in range(2):# only one run needed to show valid
            num_assignments_before = Assignment.objects.count()
            num_emails_sent_before = len(mail.outbox)
            massAssign("SP2024")
            num_assignments_after = Assignment.objects.count()
            num_emails_sent_after = len(mail.outbox)
            section = Section.objects.filter(course_number = cour5236 ).first()
            assignments = Assignment.objects.filter(student_id__in = [s1,s2,s3])
            self.assertEqual(assignments.count(),1) 

            num_assignments_made = num_assignments_after - num_assignments_before
            num_emails_sent = num_emails_sent_after - num_emails_sent_before
            self.assertEqual(num_emails_sent, (num_assignments_made * 2) + 1) # 2 emails per assignment + 1 admin email

            a1 = assignments.filter(student_id__in = [s3]).first()
            self.assertEqual(a1.student_id,s3)
            section.num_graders_needed = 2
            us1.save()
            us2.save()
            us3.save()
            a1.delete()
            section.save()

  





  
        
        
