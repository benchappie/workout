import json
import wsgiref.simple_server  
import mysql.connector
import urllib.parse
from tabulate import tabulate 
#from decouple import config
#from dotenv import load_dotenv
from getpass import getpass

# .env variable for DB credentials
# load_dotenv('workout')
USER = input('Root: ')
PASS = getpass('Password: ')     

# list of all submissions
forms_data = []  

def application(environ, start_response):
    # requested path
    path = environ["PATH_INFO"]
    # requested method
    method = environ["REQUEST_METHOD"]

    # content type of response and basic string as response
    content_type = "text/html" 

    if path == "/":
        if method == "POST":
            # getting wsgi.input object to gain info from form
            input_obj = environ["wsgi.input"]
            # length of body specified
            input_length = int(environ["CONTENT_LENGTH"])
            # get body of wsgi.input object and decoding to string
            body = input_obj.read(input_length).decode()

            # parse body of form
            data = urllib.parse.parse_qs(body, keep_blank_values=True)
            # data of body placed into dictionary format w/keys
            req = {
                "date" : data["date"][0],
                "exercise" : data["exercise"][0],
                "reps" : data["reps"][0],
                "weight" : data["weight"][0]
            }
            # adding to submission which is a list of dictionaries now - push to DB
            forms_data.append(req)
            pushDB()

            response = b"Your feedback submitted successfully."
            status = "200 OK"

        # read html file and display when nothing is submitted to form
        else:
            with open("workout_feedback.html","r") as f:
                response = f.read().encode()
            status = "200 OK"

    # create /forms path to display a json version of the form
    elif path == "/forms":
        response = json.dumps(forms_data).encode()
        status = "200 OK"
        # requires content-type change
        content_type = "application/json"

    #display latest table data when directed to /table URL 
    elif path == "/table":
        response = fetchDB() 
        status = "200 OK"

    else:
        # 404 - path not found
        response = b"<h1>Not found</h1><p>Entered path not found</p>"
        status = "404 Not Found"
    
    # define headers which will be parameters of start_response
    headers = [("Content-Type", content_type),
               ("Content-Length",str(len(response)))
    ]
    
    # tell application to start responding
    start_response(status, headers)
    return [response]

# function for DB - create connection with DB and set cursor to allow python to talk with DB
def pushDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USER, 
        password=PASS,
        database="workoutdb2",
    ) 

    cursor = mydb.cursor()

    # enter the following SQL query, for each line of form info
    for entry in forms_data: 
        values = (entry['date'], entry['exercise'], entry['reps'], entry['weight'])
        insert_set = "INSERT INTO sets (date, exercise, reps, weight) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_set, values)
        mydb.commit()

    cursor.close()
    mydb.close() 

# function for DB pull of table all inclusive list of sets
def fetchDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USER, 
        password=PASS,
        database="workoutdb2",
    ) 

    cursor = mydb.cursor()

    # print what is currently in the table for user to view
    cursor.execute("SELECT * FROM sets")
    table = cursor.fetchall()
    result = tabulate(table, tablefmt='html').encode()

    cursor.close()
    mydb.close() 
    return(result)

# simple server set up and running indefinitely
if __name__ == "__main__":
    w_s = wsgiref.simple_server.make_server(
        host="localhost",
        port=7780,
        app=application
    )
    w_s.serve_forever()