"""Get data about workouts from users, read/write to csv"""

import pandas as pd
import mysql.connector

#initialize the LISTS needed for user inputs
dates = []
names = [] 
sets = [] 
reps = [] 
weights = [] 

#initialize class to include date/name/sets/reps/weight attributes
class Exercise:
    counter = 0

    def __init__(self, date, name, sets, reps, weight):
        self.date = date
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

    #method to offload data from class to lists
    def recordExercise(self):
        dates.append(self.date)
        names.append(self.name)
        sets.append(self.sets)
        reps.append(self.reps)
        weights.append(self.weight)

#initialize flag to positive response while loop to get inputs; record exercises into LISTS
addExercise = "Y"

while addExercise == "Y":

    exercise = Exercise(input("Date: "), input("Exercise: "), input("Sets: "), input("Reps: "), input("Weight: "))
    Exercise.recordExercise(exercise)
    Exercise.counter += 1

    #provide offramp from loop
    addExercise = input("\nEnter Y if you have another exercise, N if you do not: ")
    if addExercise == "Y":
        continue
    else:
        break

#make the lists into a dictionary and make a dataframe
fitness = {'date': dates, 'name': names, 'sets': sets, 'reps': reps, 'weight': weights}
df = pd.read_csv("fitness_frame.csv", usecols=[1,2,3,4,5])
df = df.append(pd.DataFrame(fitness))

#print for viewing purposes
print(df)

#push df to csv
df.to_csv("fitness_frame.csv")