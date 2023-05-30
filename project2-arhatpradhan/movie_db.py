import sqlite3 as lite
import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sqlite3
import sys
import time
import xml


class Movie_db(object):
    def __init__(self, db_name):
        #db_name: "cs1656-public.db"
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()
    
    #q0 is an example 
    def q0(self):
        query = '''SELECT COUNT(*) FROM Actors'''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    # List all the actors (first and last name) who acted in at least one film in the 80s (1980-1990, both ends inclusive) 
    # and in at least one film in the 21st century (>=2000). Sort alphabetically, by the actor's last and first name.
    def q1(self):
        query = '''
            SELECT DISTINCT a.fname, a.lname 
            FROM ACTORS a 
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid 
            WHERE m.year >= 1980 AND m.year <= 1990
            INTERSECT
            SELECT a.fname, a.lname
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE (m.year >= 2000)
            ORDER BY a.lname, a.fname;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
        
    # List all the movies (title, year) that were released in the same year as the movie entitled "Rogue One: A Star Wars Story", but had a better rank 
    # (Note: the higher the value in the rank attribute, the better the rank of the movie). Sort alphabetically, by movie title.
    def q2(self):
        query = '''
            SELECT m.title, m.year FROM Movies m
            JOIN Movies m2 ON m.year = m2.year 
            WHERE m2.title = 'Rogue One: A Star Wars Story'
            AND m.rank > m2.rank 
            ORDER BY m.title


        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    # List all the actors (first and last name) who played in a Star Wars movie (i.e., title like '%Star Wars%') in 
    # decreasing order of how many Star Wars movies they appeared in. If an actor plays multiple roles in the same movie, 
    # count that still as one movie. If there is a tie, use the actor's last and first name to generate a full sorted order. 
    # Sort alphabetically, by the number of movies (descending), the actor's last name and first name.
    def q3(self):
        query = '''
            SELECT fname, lname, COUNT(DISTINCT m.mid) as num_movies 
            FROM Actors
            JOIN Cast c ON Actors.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE m.title LIKE '%Star Wars%'
            GROUP BY fname, lname
            ORDER BY num_movies DESC, lname, fname;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    # Find the actor(s) (first and last name) who only acted in films released before 1990. 
    # Sort alphabetically, by the actor's last and first name
    def q4(self):
        query = '''
           SELECT DISTINCT a.fname, a.lname
           FROM Actors a
           WHERE a.aid NOT IN (SELECT c.aid
                                FROM Cast c
                                JOIN Movies m ON c.mid = m.mid
                                WHERE m.year >= 1990)
            AND a.aid IN (SELECT c2.aid
                            FROM Cast c2
                            JOIN Movies m2 ON c2.mid = m2.mid
                            WHERE m2.year < 1990)
            ORDER BY a.lname, a.fname;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    # List the top 10 directors in descending order of the number of films they directed (first name, last name, number of films directed). 
    # For simplicity, feel free to ignore ties at the number 10 spot (i.e., always show up to 10 only). 
    # Sort alphabetically, by the number of films (descending), the actor's last name and first name.
    def q5(self):
        query = '''
            SELECT fname, lname, COUNT(md.mid) as num_films
            FROM Directors as d
            JOIN Movie_Director as md ON d.did = md.did
            GROUP BY fname, lname 
            ORDER BY num_films DESC, lname, fname 
            LIMIT 10;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    #Largest Cast with ties
    def q6(self):
        query = '''
            SELECT m.title, COUNT(c.aid) AS num_cast
            FROM Movies m
            JOIN Cast c ON m.mid = c.mid
            GROUP BY m.title
            HAVING COUNT(c.aid) = (SELECT COUNT(aid)
                                FROM Cast
                                WHERE mid = m.mid
                                GROUP BY mid
                                ORDER BY COUNT(aid) DESC, mid DESC)
            ORDER BY num_cast DESC, title ASC;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    # Find the movie(s) whose cast has more actors than actresses (i.e., gender=Male vs gender=Female). 
    # Show the title, the number of actors, and the number of actresses in the results. 
    # Sort alphabetically, by movie title. Hint: Make sure you account for the case of 0 actors or actresses in a movie.
    def q7(self):
        query = '''
        SELECT title,
            SUM(CASE WHEN gender = 'Male' THEN 1 ELSE 0 END) as num_actors,
            SUM(CASE WHEN gender = 'Female' THEN 1 ELSE 0 END) as num_actresses
        FROM Movies
        JOIN Cast c ON Movies.mid = c.mid
        JOIN Actors a ON c.aid = a.aid
        GROUP BY title
        HAVING num_actors > num_actresses
        ORDER BY title;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    # Find all the actors who have worked with at least 7 different directors. 
    # Do not consider cases of self-directing (i.e., when the director is also an actor in a movie), 
    # but count all directors in a movie towards the threshold of 7 directors. 
    # Show the actor's first, last name, and the number of directors he/she has worked with. 
    # Sort in decreasing order of number of directors.
    def q8(self):
        query = '''
            SELECT fname, lname, COUNT(DISTINCT md.did) as num_directors 
            FROM Actors 
            JOIN Cast c ON Actors.aid = c.aid
            JOIN Movie_Director md ON c.mid = md.mid 
            Where did NOT in (SELECT aid FROM Actors)
            GROUP BY fname, lname 
            HAVING num_directors >= 7
            ORDER BY num_directors DESC, lname, fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    # For all actors whose first name starts with a B, count the movies that he/she appeared in his/her debut year (i.e., year of their first movie). 
    # Show the actor's first and last name, plus the count. Sort by decreasing order of the count, then the first and last name.
    def q9(self):
        query = '''
            SELECT a.fname, a.lname, COUNT(*) AS movie_count
            FROM Actors a
            JOIN Cast c ON a.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            WHERE a.fname LIKE 'B%'
            AND m.year = (
                SELECT MIN(m2.year)
                FROM Movies m2
                JOIN Cast c2 ON m2.mid = c2.mid
                WHERE c2.aid = a.aid
            )
            GROUP BY a.aid, a.fname, a.lname
            ORDER BY movie_count DESC, a.fname, a.lname;
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows
    # Find instances of nepotism between actors and directors, i.e., an actor in a movie and 
    # the director having the same last name, but a different first name. 
    # Show the last name and the title of the movie, sorted alphabetically by last name and the movie title.
    def q10(self):
        query = ''' 
            SELECT DISTINCT Actors.lname, m.title
            FROM Actors
            JOIN Cast c ON Actors.aid = c.aid
            JOIN Movies m ON c.mid = m.mid
            JOIN Movie_Director md ON m.mid = md.mid
            JOIN Directors d ON md.did = d.did
            WHERE Actors.lname = d.lname
            AND Actors.fname != d.fname
            ORDER BY Actors.lname, m.title;
            
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q11(self):
        query = '''
            SELECT DISTINCT a3.fname, a3.lname
            FROM Actors a1
            JOIN Cast c1 ON a1.aid = c1.aid
            JOIN Movies m1 ON c1.mid = m1.mid
            JOIN Cast c2 ON m1.mid = c2.mid AND c2.aid != a1.aid
            JOIN Actors a2 ON c2.aid = a2.aid
            JOIN Cast c3 ON a2.aid = c3.aid AND c3.mid != m1.mid AND c3.aid != a1.aid
            JOIN Movies m2 ON c3.mid = m2.mid
            JOIN Cast c4 ON m2.mid = c4.mid
            JOIN Actors a3 ON c4.aid = a3.aid AND a3.aid != a1.aid AND a3.aid != a2.aid
            WHERE a1.fname = 'Kevin' AND a1.lname = 'Bacon'
            ORDER BY a3.lname, a3.fname


        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    # Assume that the popularity of an actor is reflected by the average rank of all the movies he/she has acted in. 
    # Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last name, 
    # the total number of movies he/she has acted, and his/her popularity score.
    # For simplicity, feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).
    def q12(self):
        query = '''
        SELECT a.fname AS first_name, a.lname AS last_name, COUNT(c.mid) AS num_movies, AVG(m.rank) AS popularity_score
        FROM Actors a
        JOIN Cast c ON a.aid = c.aid
        JOIN Movies m ON c.mid = m.mid
        GROUP BY a.fname, a.lname
        ORDER BY popularity_score DESC, last_name, first_name
        LIMIT 20;

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

if __name__ == "__main__":
    task = Movie_db("cs1656-public.db")
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
    rows = task.q8()
    print(rows)
    print()
    rows = task.q9()
    print(rows)
    print()
    rows = task.q10()
    print(rows)
    print()
    rows = task.q11()
    print(rows)
    print()
    rows = task.q12()
    print(rows)
    print()
