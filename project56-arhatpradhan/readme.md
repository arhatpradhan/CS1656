# Repository: template.project34
# Term Project

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Spring 2023  
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> Teaching Assistant: Evangelos Karageorgos  
>
> Term Project  
> Released: March 21, 2023
> **Due:   April 17, 2023**

### Description
This is the **term project** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2023 semester.

### Goal
The goal of this project is to expose you with a real data science problem, looking at the end-to-end pipeline.

### What to do
You are asked to modify a Python Jupyter notebook, called `bikes_pgh_data.ipynb`, as well as a python file called `calculations.py` that will:
* [Task 1] Access historical bike rental data for 2021 from HealthyRidePGH and summarize the rental data. Implement on `calculations.py`
* [Task 2] Create graphs to show the popularity of the different rental stations, given filter conditions. Implement on `bikes_pgh_data.ipynb`
* [Task 3] Create graphs to show the rebalancing issue. Implement on `bikes_pgh_data.ipynb`
* [Task 4] Cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering. Implement on `bikes_pgh_data.ipynb`

**Your program should not take more than 15 minutes to run**

We present the details of each task next. You are provided with a skeleton `bikes_pgh_data.ipynb` Jupyter notebook file, along with a skeleton `calculations.py` file which you should use.

### Task 1 (25 points)
Implement on `calculations.py`

In this task you will need to access historical bike rental data for 2021 from HealthyRidePGH and summarize it.

We will use historical rental data from HealthyRidePGH, available at [https://healthyridepgh.com/data/](https://healthyridepgh.com/data/) and also provided as part of this repository.
In particular, we will use data for the first three quarters of 2021:

* Q1: HealthyRideRentals2021-Q1.csv 
* Q2: HealthyRideRentals2021-Q2.csv  
* Q3: HealthyRideRentals2021-Q3.csv  

Each row in the file shows one rental transaction, indicating the bicycle ID, the source bike station (from station) and the destination bike station (to station). Worth noting:
* if there is no station ID, then this was usually a "dockless'' bike, e.g., `BIKE 70000`,  
* if a bike was "magically" moved from one station to a different one, that means this happened as a result of rebalancing, where HealthyRidePGH staff relocated the bike using a truck to address demand imbalance.   

In the `calculations.py` file, you must implement functionality that produces a "trips" DataFrame that accumulates data across all input *csv* files, a "daily_counts" table that summarizes daily rental data, and a "monthly_counts" table that summarizes monthly rental data.

* **Task 1.1** `produce_trips_table()` : The method must return a DataFrame with aggregated data across all input files. The DataFrame can have ANY columns you may find useful for the rest of the calculations, in any form, but it also MUST include the `Bikeid`, `Starttime`, `From station id` and `To station id` columns. The `Starttime` column must be properly parsed as a timestamp, although you can additionally have your own alternative versions of that column in string format if it's useful to your calculations. Note that the autograder will check for the appropriate columns on the `trips` table, NOT the data on the table. If the data on this table is wrong, the results for subsequent tasks will be wrong, and marked appropriately by the autograder.
* **Task 1.2** `calculate_daily_counts()`: The method must return a DataFrame with aggregate rental information per station per day, with columns:
  * **day** (string) : String representation of the day, formatted as (month/day/year), where month and day have *two* digits, and year has *four* digits
  * **station_id** (integer) : The station ID as an integer
  * **fromCNT** (integer) : total number of "from'' bikes at that station for that day (i.e., number of transactions with that _stationID_ in the **from** column)
  * **toCNT** (integer) : total number of "to'' bikes at that station for that day (i.e., number of transactions with that _stationID_ in the **to** column)
  * **rebalCNT** (integer) : total number of "rebalanced'' bikes for that day. See the next section for an explanation on how to compute this.

* **Task 1.3** `calculate_monthly_counts()`: The method must return a DataFrame, similar to Task 1.2, except broken down by the month, with columns:
  * **month** (string) : String representation of the month, formatted as (month/year), where month has *two* digits, and year has *four* digits
  * **station_id** (integer) : The station ID as an integer
  * **fromCNT** (integer) : total number of "from'' bikes at that station for that month (i.e., number of transactions with that _stationID_ in the **from** column)
  * **toCNT** (integer) : total number of "to'' bikes at that station for that month (i.e., number of transactions with that _stationID_ in the **to** column)
  * **rebalCNT** (integer) : total number of "rebalanced'' bikes for that month. See the next section for an explanation on how to compute this.

#### NOTES:
For simplicity, consider **Starttime** as the timestamp of every record. You should ignore **Stoptime** completely. For example, if a trip starts at 11:50 PM on Monday and ends at 12:10 AM on Tuesday, Just assume that the trip happened on Monday.

ALL subsequent tasks and calculations must depend ONLY on the return values from the `get_trips()`, `get_daily_counts()`, and `get_monthly_counts()` methods.

Be mindful on how you address missing values on the daily and monthly breakdown. For example, in the daily breakdown, for a specific day, a station may be referenced multiple times on `From station id`, but never on any `To station id`. In this case, a naïve implementation may not produce a row at all for that station, even though it would have a valid, positive *fromCNT*. You must make sure you have a row for that station, with a *toCNT* value of *0*. For combinations of day/stationID or month/stationID where there are no bike rentals, you must produce no rows.

The daily breakdown should be a DataTable, where every row contains the counts for a combination of day and station id. It must have the form **(day, station_id, fromCNT, toCNT, rebalCNT)**. For example:
||day | station_id | fromCNT | toCNT | rebalCNT|
|---| --- | --- | --- | --- | --- |
|*0*|04/25/2021| 4178 | 1 | 2 | 0 |
|*1*|04/25/2021| 4179 | 2 | 0 | 2 |



Similarly, the monthly breakdown must have rows of the form **(month, station_id, fromCNT, toCNT, rebalCNT)**. For example:

||month | station_id | fromCNT | toCNT | rebalCNT|
| --- | --- | --- | --- | --- | --- |
|*0*|04/2021| 4178 | 10 | 13 | 4 |
|*1*|04/2021| 4179 | 20 | 9 | 6 |



For those tables, the dates must be *strings* with the exact format as shown above, and on separate columns (not part of the table index). You see the row index on the very left. Also, the tables must be sorted first by day or month and then by station_id.

### How to compute the rebalancing

For every bikeID we need to figure out cases where when the data is sorted by bikeID trip start time.

Consider the following example snipet from the Q2 data:

|Trip id | Starttime | Stoptime | Bikeid | Tripduration | From station id | From station name | To station id | To station name | Usertype |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|66669783 | 4/1/2021 16:31 | 4/1/2021 17:41 | 70000 |4178	| 1047	|S 22nd St & E Carson St	|1046	|S 25th St & E Carson St	|Customer|
|67181259 | 4/6/2021 18:56	| 4/6/2021 19:08 | 70000 | 719	| 49301	|Centre Ave & N Craig St	|1024	|S Negley Ave & Baum Blvd	|Subscriber |
|67425370 | 4/8/2021 16:45	| 4/8/2021 16:50 | 70000 | 305	| 1024	|S Negley Ave & Baum Blvd	|1026	|Penn Ave & S Whitfield St	|Customer  |

The first line indicates a rental from stationID = 1047 to stationID = 1046.
The second line indicates a rental from stationID = 49301 to stationID = 1024. This implies rebalancing, as somehow this bike was taken off circulation and put back in circulation in a different station (49301) than what was dropped off by a customer/subscriber earlier (1046).
The third line indicates a rental from stationID = 1024 (where it was left off before) to stationID = 1026.

So in this case you will need to increase by one the rebalancing count for 4/6/21 for stationID = 49301.

Notes:

* The date of a rebalancing event is the one where the *From station id* has unexpectedly changed (4/6/21 in our example)
* You should not consider dockless stations (e.g., BIKE 70000) as stations; only consider as stations those with a proper stationID value.
* The first time a bike appears in the dataset should NOT count as a rebalancing event

Finally, a simple rebalancing algorithm, where you just take **rebalCNT = abs(fromCNT - toCNT)** will work as an **approximation**, since it counts as rebalancing bikes that were left at the station and not used. If you have trouble or ran out of time, this is an appropriate shortcut for partial credit (-8 points). Calculate this for the daily breakdown, and aggregate the values for the monthly rebalCNT.


### Task 2 (30 points)
Implement on `bikes_pgh_data.ipynb`

In this task you will need to create graphs to show the popularity of the different rental stations, given filter conditions.

For this task you assume two variables containing input from the user:
* **filter_month** which corresponds to the month of interest (should have a default value of "04/2021", i.e., April of 2021), and  
* **filter_stationID** which corresponds to the stationID of interest (should have a default value of 1046).  

Given the above two variables, you should create the following graphs:
* **Task 2.1** Show a bar chart for the 20 most popular bikestations when considering the number of **fromCNT** per station (for filter_month). Y axis should be the fromCNT per station, X axis should be the stationID. The first stationID corresponds to the most popular station.

* **Task 2.2** For the filter_month and for the filter_stationID show a graph that shows the distribution of bike rentals throughout the month, for that station only. Y axis should be the fromCNT for that stationID for that day, X axis would be the different days in that month (i.e., 1 - 30 for April).

* **Task 2.3** For the filter_month (e.g., April) show a graph that shows the distribution of bike rentals throughout the day, for all stations. Y axis should be the fromCNT for all stations in the filter_month, X axis would be the different hours in a day (i.e., 0 - 23).

* **Task 2.4** Compute the total number of rentals each bike had for each day (regardless of station). In other words, figure out how many times a bike was listed in the input data, for each different date. For the filter_month, show a graph that shows the 20 most popular bikes. Y axis should be the number of times a bike was rented, X axis should be the bikeID. The first bikeID corresponds to the most popular station.

### Task 3 (20 points)

Implement on `bikes_pgh_data.ipynb`

In this task you will create graphs to show the rebalancing issue.

* **Task 3.1** Show a bar chart for the 20 most popular bikestations when considering the number of **rebalCNT** per station (for filter_month). Y axis should be the rebalCNT per station, X axis should be the stationID. The first stationID corresponds to the most demanding station in terms of rebalancing.

* **Task 3.2** For the filter_month and for the filter_stationID show a graph that shows the distribution of bike rebalancing throughout the month, for that station only. Y axis should be the rebalCNT for that stationID for that day, X axis would be the different days in that month (i.e., 1 - 30 for April).

### Task 4 (25 points)

Implement on `bikes_pgh_data.ipynb`

In this task you will cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering.

For this task, you should create a data structure where for each stationID you record the following features:
* 3 variables for the total fromCNT for each station for each of the 3 months of the third quarter (i.e., 7, 8, 9)   
* 3 variables for the total rebalCNT for each station for each of the 3 months of the third quarter (i.e., 7, 8, 9)  

This creates a 6-dimensional space for the different stations.

* **Task 4.1** You should perform clustering on the above 6-dimensional space using K-means (with at least 3 different values for K) and DBSCAN  (with at least three different value combinations for min_samples and eps) [https://scikit-learn.org/stable/modules/clustering.html#clustering](https://scikit-learn.org/stable/modules/clustering.html#clustering).

* **Task 4.2** You should generate one bar chart per algorithm option (i.e., 6 different charts) showing the distribution of the number of stations per cluster. Y axis should be the number of stations in that cluster, X axis would be the clusterID. The first clusterID corresponds to the biggest cluster. Make sure each graph is properly labeled with the algorithm name and the parameters used.

* **Task 4.3** You should provide a brief explanation about your optimal choice of K. You should utilize the Elbow method on a reasonable range of K values. You should also mention (a) what is the best value of K that you found and (b) what is the best algorithm out of the two that you tried. For the second question, it is possible the results will be inconclusive.


### Important notes about grading
It is absolutely imperative that your Jupyter notebook program:  
* runs without any syntax or other errors (using Python 3)  
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss.


### Allowed Python Libraries
You are allowed to use the following Python libraries (although a fraction of these will actually be needed):
```
argparse
collections
csv
numpy
json
glob
math
matplotlib
os
pandas
re
requests
sklearn
scipy
string
sys
time
xml
```
If you would like to use any other libraries, you must ask permission within a maximum of two weeks after the assignment was released, using [canvas](http://cs1656.org).


### About your github account
* Since we will utilize the github classroom feature to distribute the assignments it is very important that your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  



### How to submit your assignment

We are going to use Gradescope to submit and grade your assignments. 

To submit your assignment:

* login to Canvas for this class <https://cs1656.org>  
* select "Term Project" from the list of active assignments (through Gradescope)
* follow the instructions to submit your assignment.

### What to submit

For this test assignment you only need to submit `bikes_pgh_data.ipynb`  and `calculations.py` to "Term Project". You must not submit any of the data files or anything else. You can modify the files and resubmit them as many times as you want until the deadline of **Monday, April 17, 11:59 pm**.

### Late submissions

For full points, we will consider the version submitted to Gradescope

- the day of the deadline **Monday, April 17, 11:59 pm**
- 24 hours later (for submissions that are one day late / -5 points), and
- 48 hours after the first deadline (for submissions that are two days late / -15 points).

Our assumption is that everybody will submit on the first deadline.  If you want us to grade a late submission, you need to email us at `cs1656-staff@cs.pitt.edu`

Wee will grade the projects even if only some of the tasks are completed (for partial credit). If you have not completed some of the tasks, please say so in the comments.