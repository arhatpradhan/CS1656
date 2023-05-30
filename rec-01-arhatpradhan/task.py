import os
from requests import get
import json
import pandas as pd
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Task(object):
    def __init__(self):
        self.response = get(
            'http://db.cs.pitt.edu/courses/cs1656/data/hours.json', verify=False)
        self.hours = json.loads(self.response.content)

    def part4(self):
        df = pd.DataFrame(self.hours)
        df.to_csv('hours.csv', index=False)

    def part5(self):
        # write output to 'part5.txt'
        df = pd.read_csv('hours.csv')
        df.to_csv('part5.txt', index=False)

    def part6(self):
        with open('hours.csv', mode = 'r') as csvfile:
            csvreader = csv.reader(csvfile) 
            with open('part6.txt', mode = 'w') as txtfile:
                for row in csvreader:
                    txtfile.write(str(row))

    def part7(self):
        with open('hours.csv', mode = 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            with open('part7.txt', 'w') as txtfile:
               # for each row
                for row in csvreader:
                    # for each cell in that row write it
                    for cell in row:
                        txtfile.write(cell)


if __name__ == '__main__':
    task = Task()
    task.part4()
    task.part5()
    task.part6()
    task.part7()
