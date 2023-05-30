import sqlite3 as lite
import csv
import re
import pandas as pd


class Task(object):
    def __init__(self, db_name):
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()

    #q0 is an example 
    def q0(self):
        query = '''
            SELECT COUNT(*) FROM students
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Provide Query that will print the first and last names
    #of all sophomore students
    def q1(self):
        query = '''
            SELECT firstName, lastName
            FROM Students
            WHERE yearStarted = 2019
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
        
    #Query that will print the first and last names of all students 
    #who either have a cs or a coe major
    def q2(self):
        query = '''
            SELECT firstName, lastName
            FROM Students
            WHERE sid IN (SELECT sid
            FROM Majors
            WHERE major IN ('CS', 'COE'))
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    
    #Query that will generate the # of students who have astro sa their major
    def q3(self):
        query = '''
            SELECT COUNT(DISTINCT sid)
            FROM Majors
            WHERE major = 'ASTRO';
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    #Provide the query that will generate the first name, last name, year started
    #and the total # of credits for every student
    #Do not consider courses with a 0 bc these are failed courses
    def q4(self):
        query = '''
        SELECT 
            Students.firstName,
            Students.lastName,
            Students.yearStarted,
            SUM(Grades.credits) as total_credit                                                                                                                                                                             s
        FROM Students 
        JOIN Grades ON Students.sid = Grades.sid
        WHERE 
            Grades.grade != 0
         GROUP BY 
            Students.sid
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Query that will generate the professor name and how many courses that professor has taught,
    #for every professor
    def q5(self):
        query = '''
            SELECT 
                Courses.professor,
                COUNT(Courses.cid) as total_courses
            FROM 
                Courses 
            GROUP BY 
                Courses.professor
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Distribution of each grades, how many 4s, 3s, 2s, 1s
    def q6(self):
        query = '''
            SELECT 
                Courses.cid, Grades.grade, COUNT(Grades.grade) AS count
            FROM 
                Courses
            JOIN 
                Grades ON Courses.cid = Grades.cid
            GROUP BY 
                Courses.cid, Grades.grade

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Same query as 6 but only for A grades
    def q7(self):
        query = '''
        SELECT 
            Courses.cid, Grades.grade, COUNT(Grades.grade) AS count
        FROM 
            Courses
            JOIN Grades ON Courses.cid = Grades.cid
        WHERE 
            Grades.grade = 4
        GROUP BY 
            Courses.cid, Grades.grade
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

if __name__ == "__main__":
    task = Task("students.db")
    rows = task.q0()
    print(rows)
    print()
    rows = task.q1()
    print(rows)
    print()
    rows = task.q2()
    print(rows)
    print()
    rows = task.q3()
    print(rows)
    print()
    rows = task.q4()
    print(rows)
    print()
    rows = task.q5()
    print(rows)
    print()
    rows = task.q6()
    print(rows)
    print()
    rows = task.q7()
    print(rows)
    print()
