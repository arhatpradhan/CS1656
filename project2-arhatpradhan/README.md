# Repository: template.project2
# Assignment #2: SQL  

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Spring 2023    
> Instructor: Alexandros Labrinidis  
> Teaching Assistant: Evangelos Karageorgos

> Assignment: #2
> Released: Feb 6, 2023  
> **Due: Feb 22, 2023**

### Description
This is the **second assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

### Goal
The goal of this assignment is for you to gain familiarity with SQL.

---

### What to do -- movie_db.py

In this assignment you are asked to provide SQL queries that answer 12 questions.

The provided skeleton Python script includes database connection commands and also includes commands to run the SQL queries and return their output. What you should update are the the queries themselves.

### Database

The database you are provided with is an SQLite database, stored in the file `cs1656-public.db`. The schema of the database is as follows:
* Actors (aid, fname, lname, gender)  
* Movies (mid, title, year, rank)  
* Directors (did, fname, lname)  
* Cast (aid, mid, role)  
* Movie_Director (did, mid)  

During grading, your queries will be tested against this public database, but they will be also tested against a database that is kept private.


### Queries

You are asked to provide SQL queries that provide answers for the following questions. Note that **actors** refers to both male and female actors, unless explicitly specified otherwise. Also note that you should not rely on the data provided in the public database for any of the answers; the private database will have more data. Finally, please note that you may define views, etc., as part of other queries.

* **[Q01]** List all the actors (first and last name) who acted in at least one film in the 80s (1980-1990, both ends inclusive) and in at least one film in the 21st century (>=2000). Sort alphabetically, by the actor's last and first name.

* **[Q02]** List all the movies (title, year) that were released in the same year as the movie entitled `"Rogue One: A Star Wars Story"`, but had a better rank (Note: the higher the value in the *rank* attribute, the better the rank of the movie). Sort alphabetically, by movie title.  

* **[Q03]** List all the actors (first and last name) who played in a Star Wars movie (i.e., title like '%Star Wars%') in decreasing order of how many Star Wars movies they appeared in. If an actor plays multiple roles in the same movie, count that still as one movie. If there is a tie, use the actor's last and first name to generate a full sorted order. Sort alphabetically, by the number of movies (descending), the actor's last name and first name.  

* **[Q04]** Find the actor(s) (first and last name) who **only** acted in films released before 1990. Sort alphabetically, by the actor's last and first name.  

* **[Q05]** List the top 10 directors in descending order of the number of films they directed (first name, last name, number of films directed). For simplicity, feel free to ignore ties at the number 10 spot (i.e., always show up to 10 only). Sort alphabetically, by the number of films (descending), the actor's last name and first name.  

* **[Q06]** Find the top 10 movies with the largest cast (title, number of cast members) in decreasing order. Note: show all movies in case of a tie.  

* **[Q07]** Find the movie(s) whose cast has more actors than actresses (i.e., gender=Male vs gender=Female).  Show the title, the number of actors, and the number of actresses in the results. Sort alphabetically, by movie title. Hint: Make sure you account for the case of 0 actors or actresses in a movie.

* **[Q08]** Find all the actors who have worked with at least 7 different directors. Do not consider cases of self-directing (i.e., when the director is also an actor in a movie), but count all directors in a movie towards the threshold of 7 directors. Show the actor's first, last name, and the number of directors he/she has worked with. Sort in decreasing order of number of directors.

* **[Q09]** For all actors whose first name starts with a **B**, count the movies that he/she appeared in his/her debut year (i.e., year of their first movie). Show the actor's first and last name, plus the count. Sort by decreasing order of the count, then the first and last name.  

* **[Q10]** Find instances of nepotism between actors and directors, i.e., an actor in a movie and the director having the same last name, but a different first name. Show the last name and the title of the movie, sorted alphabetically by last name and the movie title.  

* **[Q11]** The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the *"co-acting"* graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2 (first name, last name). Sort the results by the last and first name. You can familiarize yourself with the concept, by visiting [The Oracle of Bacon](https://oracleofbacon.org).  

* **[Q12]** Assume that the *popularity* of an actor is reflected by the average *rank* of all the movies he/she has acted in. Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last name, the total number of movies he/she has acted, and his/her popularity score. For simplicity, feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).  

---

### Important notes about grading
It is absolutely imperative that your python program:  
* runs without any syntax or other errors (using Python3) 
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss.


### Allowed Python Libraries
You are allowed to use the following Python libraries (although a fraction of these will actually be needed):
```
argparse
collections
csv
json
glob
math
os
pandas
re
requests
string
sys
time
xml
```
If you would like to use any other libraries, you must ask permission within a maximum of one week after the assignment was released, using [canvas](http://cs1656.org).


### How to submit your assignment
We are going to use Gradescope to submit and grade your assignments. 

To submit your assignment:
* login to Canvas for this class <https://cs1656.org>  
* click on Gradescope from the menu on the left  
* select "Assignment #2" from the list of active assignments in Gradescope
* follow the instructions to submit your assignment and have it automatically graded.

### What to submit
For this test assignment you only need to submit `movie_db.py` to "Assignment #2" and see if you get all 120 points. In case of an error or wrong result, you can modify the file and resubmit it as many times as you want until the deadline of **Wednesday, February 22, 11:59 pm**.

### Late submissions
For full points, we will consider the version submitted to Gradescope 
* the day of the deadline **Wednesday, February 22, 11:59 pm**  
* 24 hours later (for submissions that are one day late / -5 points), and  
* 48 hours after the first deadline (for submissions that are two days late / -15 points).

Our assumption is that everybody will submit on the first deadline. If you want us to grade a late submission, you need to email us at `cs1656-staff@cs.pitt.edu`

### About your github account
Since we will utilize the github classroom feature to distribute the assignments it is very important that your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
