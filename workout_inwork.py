"""Get data about workouts from users, read/write to DB. 'Sets' are fundamental unit of input"""

import pandas as pd
import mysql.connector
from getpass import getpass
import numpy as np

#initialize the LISTS needed for user inputs
dates = []
exercises = [] 
reps = [] 
weights = [] 

#initialize class to include date/name/reps/weight attributes
class Set:
    counter = 0

    def __init__(self, date, exercise, reps, weight):
        self.date = date
        self.exercise = exercise
        self.reps = reps
        self.weight = weight

    #method to offload data from class to lists
    def recordSet(self):
        dates.append(self.date)
        exercises.append(self.exercise)
        reps.append(self.reps)
        weights.append(self.weight)

#initialize flag to positive response while loop to get inputs; record exercises into LISTS
addExercise = "Y"

while addExercise == "Y":

    set = Set(input("Date: "), input("Exercise: "), input("Reps: "), input("Weight: "))
    Set.recordSet(set)
    Set.counter += 1

    #provide offramp from loop
    addSet = input("\nEnter Y if you have another set, N if you do not: ")
    if addSet == "Y":
        continue
    else:
        break

#use the zip function to create a list of tuples
zipped_sets = list(zip(dates, exercises, reps, weights))

#create connection with DB and set cursor to allow python to talk with DB
mydb = mysql.connector.connect(
    host="localhost",
    user=input("Enter username: "),
    password=getpass("Enter password: "),
    database="workoutdb2",
) 

cursor = mydb.cursor()

#using a sql formula, enter the following SQL query, for each line of inputting the zipped values
insert_set = "INSERT INTO sets (date, exercise, reps, weight) VALUES (%s, %s, %s, %s)"

for values in zipped_sets:
    cursor.execute(insert_set, values)

mydb.commit()

#print what is currently in the table for user to view
cursor.execute("SELECT * FROM sets")
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
mydb.close()

