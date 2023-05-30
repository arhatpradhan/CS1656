import sqlite3 as lite

import csv
import re
import pandas as pd
import pandas
from sqlalchemy import create_engine

class Task(object):
    def __init__(self, db_name, students, grades, courses, majors):
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()

        self.cur.execute('DROP TABLE IF EXISTS Courses')
        self.cur.execute("CREATE TABLE Courses(cid INT, number INT, professor TEXT, major TEXT, year INT, semester TEXT)")

        self.cur.execute('DROP TABLE IF EXISTS Majors')
        self.cur.execute("CREATE TABLE Majors(sid INT, major TEXT)")

        self.cur.execute('DROP TABLE IF EXISTS Grades')
        self.cur.execute("CREATE TABLE Grades(sid INT, cid INT, credits INT, grade INT)")

        self.cur.execute('DROP TABLE IF EXISTS Students')
        self.cur.execute("CREATE TABLE Students(sid INT, firstName TEXT, lastName TEXT, yearStarted INT)")

        engine = create_engine("sqlite:///"+db_name)
        df1 = pd.read_csv(students)
        df1.to_sql('students', engine, if_exists='append', index=False)

        df2 = pd.read_csv(grades)
        df2.to_sql('grades', engine, if_exists='append', index=False)

        df3 = pd.read_csv(courses)
        df3.to_sql('courses', engine, if_exists='append', index=False)

        df4 = pd.read_csv(majors)
        df4.to_sql('majors', engine, if_exists='append', index=False)

        self.cur.execute("DROP VIEW IF EXISTS allgrades")
        self.cur.execute("""
        create view allgrades as
        SELECT s.firstName, s.lastName, m.major as ms, 
               c.number, c.major as mc, g.grade 
        FROM students as s, majors as m, grades as g, courses as c
        WHERE s.sid = m.sid AND g.sid = s.sid AND g.cid = c.cid
        """)


    #q0 is an example  
    def q0(self):
        query = '''
            SELECT * FROM students
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Show how many courses were passed (grade > 0) per student per semester (plus
    #year). Show student id, year, semester and the count. Sort the results by student id,
    #year and semester.
    def q1(self):
        query = '''
            SELECT students.sid, courses.year, courses.semester, COUNT(grades.grade)
            FROM students
            JOIN grades ON students.sid = grades.sid
            JOIN courses ON grades.cid = courses.cid
            WHERE grades.grade > 0
            GROUP BY students.sid, courses.year, courses.semester
            ORDER BY students.sid, courses.year, courses.semester;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Same as T1, but show student first and last name instead of student id. Also only
    #show results for students passing at least two courses for every semester. Sort the
    #results by first name, last name, year and semester.
    def q2(self):
        query = '''
            SELECT students.firstName, students.lastName, courses.year, courses.semester, COUNT(grades.grade)
            FROM students
            JOIN grades ON students.sid = grades.sid
            JOIN courses ON grades.cid = courses.cid
            WHERE grades.grade > 0
            GROUP BY students.firstName, students.lastName, courses.year, courses.semester
            HAVING COUNT(grades.grade) >= 2
            ORDER BY students.firstName, students.lastName, courses.year, courses.semester;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Show the students that have failed at a course in their majors (firstName, last-
    #Name, major, courseNumber), utilizing the ‘allgrades’ view. Sort the results by first
    #name, last name, major and courseNumber.
    def q3(self):
        query = '''
            SELECT firstName, lastName, ms as major, number as courseNumber
            FROM allgrades
            WHERE grade = 0 AND ms = mc
            ORDER BY firstName, lastName, major, courseNumber;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Same as Q3 but without using the view
    def q4(self):
        query = '''
            SELECT students.firstName, students.lastName, majors.major, courses.number as courseNumber
            FROM students
            JOIN majors ON students.sid = majors.sid
            JOIN grades ON students.sid = grades.sid
            JOIN courses ON grades.cid = courses.cid
            WHERE grades.grade = 0 AND majors.major = courses.major
            GROUP BY students.firstName, students.lastName, majors.major, courses.number
            ORDER BY students.firstName, students.lastName, majors.major, courses.number;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Show the professors in decreasing order of ‘success’ (professor, success). Success
    #will be defined as the number of students passing any of the courses with grade >=
    #2. Sort by success in descending order and professor in ascending order.
    def q5(self):
        query = '''
            SELECT professor, COUNT(*) as success
            FROM courses
            JOIN grades ON courses.cid = grades.cid
            WHERE grades.grade >= 2
            GROUP BY professor
            ORDER BY success DESC, professor ASC;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    # Show a report of the courses (course_number, student_names, avg_grade). Col-
    # umn ‘student_names’ will contain the first and last names (seperated by a space) of 9
    # all students taking the course, each name being seperated by ‘,’ (eg. ‘John Doe, Mary
    # Jane’). Only students that passed a specific course (grade>=2) will be considered.
    # Also, the report should only contain courses with avg_grade > 3. Sort the results by
    # avg_grade (descending order), student_names and course_number. 
    def q6(self):
        query = '''
        SELECT c.number as course_number, group_concat(s.firstName || ' ' || s.
        lastName, ', ') as student_names, avg(g.grade) as avg_grade
        FROM students s, courses c, grades g
        WHERE g.sid=s.sid and g.cid=c.cid and g.grade>=2.0
        GROUP BY c.number
        HAVING avg_grade > 3
        order by avg_grade desc, student_names, course_number

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
        
if __name__ == "__main__":
    task = Task("database.db", 'students.csv', 'grades.csv', 'courses.csv', 'majors.csv')
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


