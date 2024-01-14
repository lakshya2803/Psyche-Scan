from flask import Flask, render_template, request, redirect, flash,session,send_file,url_for
from pymongo import MongoClient
import pandas as pd
import json
import csv,os
# importing the data cleaning file 
import backend
#date wala function
from datetime import datetime,date
# importing the sentiment analyzer file 
from sentiment import analyze_sentiment_for_user

app = Flask(__name__)
app.secret_key = 'poiuytrewq'

# MongoDB Connection String
mongoURI = 'mongodb://localhost:27017/'  

# Connecting to MongoDB
client = MongoClient(mongoURI)
db = client.psychescan  
collection = db.users  

# this is to load front page 
@app.route('/')
def home():
    return render_template('index.html')

# This is to load how it works page 
@app.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

# this will load the remedies page
@app.route('/remedies')
def remedies():
    return render_template('remedies.html')

# this will load the professional help page 
@app.route('/psy')
def psy():
    return render_template('psy.html')

@app.route('/prohelp')
def prohelp():
    return render_template('prohelp.html')

# this will load the suggestions page
@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

# this will load the home page after successful login
@app.route('/home')
def main():
    user_id = session.get('user_id')
    backend.data_cleaning()
    print(user_id)
    # sentiment.sentiment_analyzer()
    result = analyze_sentiment_for_user(user_id)
    #retrieving the currentmh value from session
    currentmh = session.get('currentmh')
    sum_of_ans = session.get('sum_of_ans')
    generate_csv(user_id)
    random_values = ycordinate(user_id)
    print("Values in array random_values :", random_values)
    num_entries1 = len(random_values)
    print("Number of Entries in random_values array :", num_entries1)
    dateofT = get_date_for_user(user_id)
    print("Date Array:", dateofT)
    dateofT_json = json.dumps(dateofT)
    num_entries = len(dateofT)
    print("Number of Entries in dateofT array :", num_entries)
    random_values2 = convert_to(random_values)
    print("New Random values in percentage are: ",random_values2)
    print("number of entries in new random array: ",len(random_values2))
    phq_value = convert_to_percentage(sum_of_ans,1,27)
    print("The phq9 score in percentage: ",phq_value)
    average_sentiment_score = session.get('average_sentiment_score')
    avg_senti = convert_to_percentage(average_sentiment_score,1,-1)
    print("Average value of sentiment in percentage: ",avg_senti)
    final_coordinate = session.get('final_coordinate')
    final_coord = convert_to_percentage(final_coordinate,1,-1)
    print("Value of final coordinate in percentage: ",final_coord)
    return render_template('main.html',random_values = random_values2,dateofT = dateofT_json,avg_pie =avg_senti,phq_pie=phq_value,fc_pie=final_coord)

def ycordinate(user_id):
    # Initialize an empty list to store the values from 'sentiment_score' column
    random_values = []

    # Load the CSV file for sentiment scores
    vader_data = pd.read_csv(f"analyzedDataFinalProduct2_{user_id}.csv")

    # Get the number of rows in the sentiment scores CSV file
    total_rows_sentiment = vader_data.shape[0]

    # Increment counter
    increment_counter = 25

    # Iterate through the CSV file and insert values at intervals of 25
    for i in range(0, total_rows_sentiment):
        # Check if the index is a multiple of the increment_counter
        if i % increment_counter == 0:
            # Extract the value from the 'sentiment_score' column
            value = vader_data['sentiment_score'].iloc[i]
            # Append the value to the random_values list
            random_values.append(value)

    # Reverse the random_values array
    random_values.reverse()
    # Load the CSV file for the last value
    graph_data = pd.read_csv(f"graph_help_{user_id}.csv")

    # Get the last value from the 'final_coordinate' column
    last_value = graph_data['final_coordinate'].iloc[0]

    # Add the last value to the random_values array
    random_values.append(last_value)

    # Print or use random_values as needed
    print(random_values)
    return random_values

def get_date_for_user(user_id):
    # Load the CSV file 'cleanedData1.csv'
    csv_file_path = 'cleanedData1.csv'
    
    if not os.path.exists(csv_file_path):
        return 'CSV file not found: cleanedData1.csv'

    try:
        cleaned_data = pd.read_csv(csv_file_path)

        # Filter rows based on user_id
        user_data = cleaned_data[cleaned_data['user_id'] == user_id]

        # Check if 'post_created' column exists in the filtered DataFrame
        if 'post_created' not in user_data.columns:
            return f"'post_created' column not found for user ID: {user_id}"

        # Increment counter for date intervals
        increment_counter = 25

        # Initialize an empty list to store the values from 'post_created' column
        dateofT = []

        # Iterate through the rows and insert values at intervals of 25
        for i in range(0, len(user_data)):
            # Check if i is a multiple of increment_counter
            if i % increment_counter == 0:
                # Extract the value from the 'post_created' column
                value = user_data['post_created'].iloc[i]
                
                # Convert the value to the desired format
                formatted_date = datetime.strptime(value, '%a %b %d %H:%M:%S +0000 %Y').strftime('%b %d')

                # Append the formatted_date to the dateofT list
                dateofT.append(formatted_date)

       # Reverse the dateofT array
        dateofT.reverse()
       
       # Add the current date to dateofT in the desired format
        current_date = date.today().strftime('%b %d')
        dateofT.append(current_date)

        return dateofT
    except Exception as e:
        return f'Error reading CSV: {str(e)}'

# def avg():
    

def convert_to(random_values):
    random = []
    for r in random_values:
        random.append(convert_to_percentage(r,1,-1))

    return random

def convert_to_percentage(value, max_range,min_range):
    
    # Convert the value to percentage scale
    percentage = abs(round(((value - min_range) / (max_range - min_range)) * 100, 2))

    percentage = max(min(percentage, 100), 0)
    return percentage


# this is to load phq9 form 
@app.route('/phq9', methods=['GET','POST'])
def phq9():
    if request.method == 'POST':
        q1 = int(request.form['q1'])
        q2 = int(request.form['q2'])
        q3 = int(request.form['q3'])
        q4 = int(request.form['q4'])
        q5 = int(request.form['q5'])
        q6 = int(request.form['q6'])
        q7 = int(request.form['q7'])
        q8 = int(request.form['q8'])
        q9 = int(request.form['q9'])

        
        sum_of_ans = q1+q2+q3+q4+q5+q6+q7+q8+q9
        # Set currentmh based on the value of sum_of_ans
        if 1 <= sum_of_ans <= 4:
            currentmh = 0.87
        elif 5 <= sum_of_ans <= 9:
            currentmh = 0.62
        elif 10 <= sum_of_ans <= 14:
            currentmh = 0
        elif 15 <= sum_of_ans <= 19:
            currentmh = -0.62
        elif 20 <= sum_of_ans <= 27:
            currentmh = -0.87
        else:
            # Handle other cases as needed
            currentmh = 0.93

        #storing the currentmh in session for further use
        session['currentmh'] = currentmh
        session['sum_of_ans'] = sum_of_ans
        return redirect('/home')
    return render_template('form.html')

#graph wala code
@app.route('/generate_csv/<user_id>', methods=['GET','POST'])
def generate_csv(user_id):
    # Get average sentiment score from the corresponding CSV file
    csv_file_path = f'all_sentiment_score3_{user_id}.csv'
    if not os.path.exists(csv_file_path):
        return 'CSV file not found for the specified user ID.'

    df = pd.read_csv(csv_file_path)
    average_sentiment_score = df['average_sentiment_score'].iloc[0]

    session['average_sentiment_score'] = average_sentiment_score

    # Retrieve currentmh value from session
    currentmh = session.get('currentmh', 0)

    # Calculate final coordinate
    final_coordinate = (average_sentiment_score + currentmh) / 2
    session['final_coordinate'] = final_coordinate

    # Create a new CSV file with the final coordinate
    csv_output_path = f'graph_help_{user_id}.csv'
    with open(csv_output_path, 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'final_coordinate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'user_id': user_id, 'final_coordinate': final_coordinate})

    return send_file(csv_output_path, as_attachment=True)

# this is to load login page, it will check the credintial from the
# database and login 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        user = collection.find_one({'user_id': user_id})

        if collection.find_one({'user_id': user_id}):   
            if user and user['password'] == password:
                # storing user_id in session for further use
                session['user_id'] = user_id
                # Flash a success message and redirect to home
                flash('Login successful!', 'success')
                return render_template('loading.html')
            else:
                # Flash an error message and redirect to the login page
                flash('Incorrect username or password', 'error')
                return redirect('/')
        else:
            return 'Invalid credentials. User not found.'
        
    return render_template('login.html')

# This is the section for sign up page it will load sign up page and store
# the data in mongodb database
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = request.form.get('userId')
        email_id = request.form.get('email_Id')
        age = request.form.get('age')
        gender = request.form.get('gender')
        create_password = request.form.get('createPassword')
        confirm_password = request.form.get('confirmPassword')

        # Check if username is not null
        if user_id == "":
            return "User ID cannot be empty"
        # Check if passwords match
        if create_password != confirm_password:
            return 'Passwords do not match!'

        # Check if user already exists in the database
        if collection.find_one({'user_id': user_id}):
            return 'User already exists. Please choose a different User ID.'

        collection.insert_one({'name': name, 'user_id': user_id, 'password': create_password, 
                               'email_id': email_id, 'Age':age,'Gender':gender})
        flash("signup successful","success")
        return redirect('/login')

    return render_template('signup.html')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    user = collection.find_one({'user_id': user_id})
    print(user)
    return render_template("profile.html",user=user)

@app.route('/logout')
def logout():
    # Clear user session
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
