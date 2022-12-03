"""create a program that allows the user to enter workouts, exercises, file those results, track useful history and get workout recommendations
FORAC: 
-create a file to store the workout and exercise details in organized fashion
-every time program is run, workout list, exercise list, and exercise catalog needs to be stored to the file
-screen user inputs for dates, ensure only correct date format is accepted
-only add new exercises to the exercise_catalog
-ask the user if they want to plan a workout, if so, offer to generate a list of exercises, and uncommon exercises (top 3) to consider"""


#create a class for tracking workouts taking date as input and including an index number for every workout
class Workout:
    
    #use a counter to keep track of how many times an instance has been made, and a list to store workout instances
    counter = 1
    workout_list = []

    #initialize the class with date as input, set index to counter variable
    def __init__(self, date):
        self.date = date
        self.index = Workout.counter
    
    #method to give a string for output of the index number and date of workouts
    def __str__(self):
        return "Workout {} || Date: {}".format(self.index, self.date)

    #method for displaying the date of the latest workout and the overall number of workouts completed
    def displayWorkout(self):
        return("\nYou are up to " + str(self.index) + " workouts as of " + str(self.date) + ".\n")


#create a class for tracking exercises 1) within a specific workout and 2) ongoing catalog of all exercises ever done
class Exercise(Workout):

    #initiate a list to hold the items from the workout at hand
    exercise_list = []

    #initiate a list to catalog every type of exercise ever done
    exercise_catalog = []

    #initialize the class to include name/sets/reps/weight as attributes received from user input
    def __init__(self, name, sets, reps, weight, date):

        #bring in date attribute from Workout class
        super().__init__(date)
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight
        #append exercise catalog with only the name of the exercise
        Exercise.exercise_catalog.append(self.name)

    #create an output string for exercises during occuring during the current workout
    def __str__(self):
        return "You did {}: {} sets of {} reps at {} pounds.".format(self.name, self.sets, self.reps, self.weight)


#initialize flag to positive response in prep for workout loop
addWorkout = "Y"

#while loop to gain inputs for workout class; presumably today's workout is prompted initially; nested while loop to gain exercises
while addWorkout == "Y":
    
    #get date of current workout and append to the workout list; advance counter
    workout = Workout(input("\nWorkout date (YYYYMMDD): "))
    Workout.workout_list.append(workout)
    Workout.counter += 1
  
    #prep another flag for another while loop
    addExercise = "Y"
    
    #use while loop to get as many exercises as needed including name/set/rep/weight for exercise
    while addExercise == "Y":
        
        #obtain the inputs for exercise as well as the inherited input (date) covered in the variable workout; add current exercise data to exercise_list
        exercise = Exercise(input("\nExercise: "), input("Sets: "), input("Reps: "), input("Weight: "), workout)
        Exercise.exercise_list.append(exercise) 
        
        addExercise = input("\nEnter Y if you have another exercise, or N if you do not: ")
        if addExercise == "Y":
            continue
        else:
            #print the list of exercises for this workout 
            for exercise in Exercise.exercise_list:
                print(exercise)
                    
            #when no longer accepting exercise data for current workout, clear the exercise list
            Exercise.exercise_list.clear() 
            break
    
    #user is asked if they have any other past workouts to document
    addWorkout = input("\nEnter Y if you want to document a workout from another day, or N if you do not: ")
    if addWorkout == "Y":
        continue
    else:
        break


#call the method from the workout class giving the total number of workouts/latest date
print(workout.displayWorkout())

#print the all inclusive list of workouts
print([str(workout) for workout in Workout.workout_list])

#print the all inclusive list (catalog) of exercises
print([str(exercises) for exercises in Exercise.exercise_catalog])