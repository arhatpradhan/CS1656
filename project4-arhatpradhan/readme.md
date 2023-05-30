# Repository: template.project4
# Assignment #4 -- Graph Databases

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Spring 2023    
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> Teaching Assistant: Evangelos Karageorgos
>
> Assignment: #4  
> Released: March 28, 2023  
> **Due:    April 10, 2023**

### Description
This is the **fourth assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

### Goal
The goal of this assignment is for you to gain familiarity with Graph Databases in general, and with Neo4j and, its query language, Cypher, in particular.

---

### What to do

In this assignment you are asked to:  
* download neo4j locally,  
* Set up the Movies database locally,   
* provide Cypher queries that answer 8 questions, and        
* Modify a Python script ('movie_queries.py') that will run your solutions for the 8 queries and return the results.

### Database Model

We will use the Movies database in `Recitation 9`, which has the following node labels:
* Actor  
* Director  
* Movie  
* Person  
* User  
and the following relationship types (i.e., edge labels):
* ACTS_IN  
* DIRECTED  
* FRIEND  
* RATED  

The nodes in the Movies database have a number of attributes, including the following:
* name (for Actor/Director/Person/User)  
* birthday (for Actor/Director/Person/User)  
* title (for Movie)  
* genre (for Movie)  


### Setup

You are asked to follow the installation instructions and to utilize the lab material provided through `Recitation 9`. This will enable you to have a locally running neo4j server, along with an interactive query interface. You will also be able to download the Movies database directly into neo4j.

Please note that although we will use the same database model for testing your submissions. However, it will not necessarily be identical to the one you will download.


### Connecting to neo4j using Python

As part of this repository, you are provided with a sample Python script (movie_queries.py`) that connects to the local graph database (which you have established by following the previous steps).


### Queries

You are asked to provide Cypher queries that provide answers for the following questions. Note that **actors** refers to both male and female actors, unless explicitly specified otherwise.

* **[Q1]** List the first 20 actors in descending order of the number of films they acted in. Sort by the number of films in descending order, and the actor's name in ascending order.  
*OUTPUT*: actor_name, number_of_films_acted_in


* **[Q2]** Find the movie with the largest cast, out of the list of movies that have a review.  
*OUTPUT*: movie_title, number_of_cast_members
* **[Q3]** Show which directors have directed movies in at least 2 different genres. Sort by the number of genres in descending order, and the director's name in ascending order.  
    *OUTPUT*: director name, number of genres
* **[Q4]** The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the *"co-acting"* graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. *List all actors whose Bacon number is exactly 2* (first name, last name).
  You can familiarize yourself with the concept, by visiting [The Oracle of Bacon](https://oracleofbacon.org).
  Don't return duplicates. Sort by the Actor's name.  
  *OUTPUT*: actor_name


### Output Format (ignore at your own risk!)

The provided skeleton code takes care of connecting to the database, executing the queries and returning the results in the expected format, a list of tuples for the records. You only need to write the correct queries.

For example, for the following question:

Q0: show the 3 oldest actors in the database, with the oldest one first.  
*OUTPUT*: name, id

The corresponding Cypher query should be:
```
MATCH (n:Actor) RETURN n.name, n.id ORDER BY n.birthday ASC LIMIT 3
```

The method for it should be as follows:
```
def q0(self):
	result = self.transaction.run("""
		MATCH (n:Actor) RETURN n.name, n.id ORDER BY n.birthday ASC LIMIT 3
	""")
	return [(r[0], r[1]) for r in result]
```

The result returned is the list:
```
[('Claudia Cardinale', '4959'),('Oliver Reed', '936'), ('Anthony Hopkins', '4173')]
```

---


### Important notes about grading
It is absolutely imperative that your python program:  

* runs without any syntax or other errors (using Python3) 
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss.


### Allowed Python Libraries
You are allowed to use the following Python libraries:
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

---

### How to submit your assignment
We are going to use Gradescope to submit and grade your assignments. 

To submit your assignment:

* login to Canvas for this class <https://cs1656.org>  
* select "Assignment #4" from the list of active assignments (through Gradescope)
* follow the instructions to submit your assignment and have it automatically graded.

### What to submit

For this test assignment you only need to submit `movie_queries.py` to "Assignment #4" and see if you get all 100 points. In case of an error or wrong result, you can modify the file and resubmit it as many times as you want until the deadline of **Monday, April 10, 11:59 pm**.

### Late submissions

For full points, we will consider the version submitted to Gradescope 

* the day of the deadline **Monday, April 10, 11:59 pm**  
* 24 hours later (for submissions that are one day late / -5 points).
* 48 hours later (for submissions that are two days late / -15 points).

Our assumption is that everybody will submit on the first deadline. If you want us to grade a late submission, you need to email us at `cs1656-staff@cs.pitt.edu`


### About your github account
* Since we will utilize the github classroom feature to distribute the assignments it is very important that your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  

