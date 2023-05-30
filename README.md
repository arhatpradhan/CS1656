# CS1656
A collection of projects and labs done in the class Intro to Data Science
## Project 1

Description
This is the first assignment for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

Goal
The goal of this assignment was to get familiar with Python and also get exposed to real data.

Task-- pittbikes.py
You are asked to complete a Python program, called pittbikes.py that will access live data from a City Bike Share System and provide answers to specific queries about shared bike availability in the Pittsburgh region.

The program contains a class, Bike, that has three arguments in its constructor, baseURL, station_info and station_status. These arguments are used to define URLs for specific data feeds, namely information about individual stations and the status of every station. You can create an instance of the Bike class by calling its constructor with appropriate URL fragments, and call its methods to run the different parts of the assignment.

## Project 2 
Description
This is the second assignment for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

Goal
The goal of this assignment was to gain familiarity with SQL.

Task -- movie_db.py
In this assignment we are asked to provide SQL queries that answer 12 questions.

The provided skeleton Python script includes database connection commands and also includes commands to run the SQL queries and return their output.

## Project 3

Description
This is the third assignment for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

Goal
The goal of this assignment is to get familiar with  User-based Recommender Systems and also exposed me to model evaluation on real data.

Task -- recommender.py
You are asked to complete a Python program, called recommender.py that will

[Task 1] Calculate user similarity weights among users using four different metrics, including Euclidean distance, Manhattan distance, Pearson correlation, and Cosine similarity
[Task 2] Use user similarity weights from top k users to predict movies ratings for selected users
[Task 3] Evaluate the performances of combinations of different metrics and different values of k

## Project 4 
Description
This is the fourth assignment for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

Goal
The goal of this assignment is to gain familiarity with Graph Databases in general, and with Neo4j and, its query language, Cypher.

What to do
In this assignment you are asked to:

1. Download neo4j locally
2. Set up the Movies database locally,
3. Provide Cypher queries that answer 8 questions, and
4. Modify a Python script ('movie_queries.py') that will run your solutions for the 8 queries and return the results.

## Term Project
Description
This is the term project for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

Goal
The goal of this project is to get exposed to a real data science problem, looking at the end-to-end pipeline.

What to do
You are asked to modify a Python Jupyter notebook, called bikes_pgh_data.ipynb, as well as a python file called calculations.py that will:

[Task 1] Access historical bike rental data for 2021 from HealthyRidePGH and summarize the rental data. Implement on calculations.py
[Task 2] Create graphs to show the popularity of the different rental stations, given filter conditions. Implement on bikes_pgh_data.ipynb
[Task 3] Create graphs to show the rebalancing issue. Implement on bikes_pgh_data.ipynb
[Task 4] Cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering. Implement on bikes_pgh_data.ipynb
