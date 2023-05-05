import sqlite3
import re
import time
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('projects.db')
c = conn.cursor()

# Create the users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              last_name TEXT,
              email TEXT,
              password TEXT,
              mobile TEXT)''')
conn.commit()

def check_string(message):
    while True:
        string = input(message)
        if string.isalpha():
            return string
        else:
            print("Please Enter a valid string.")

def check_int(message):
    while True:
        string = input(message)
        if string.isdigit():
            return int(string)
        else:
            print("Please Enter a valid integer.")

def check_email(message):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    while True:
        email = input(message)
        if re.fullmatch(regex, email):
            return email
        else:
            print("Please Enter a valid email address.")

def is_equal(password, message):
    while True:
        confirm_password = input(message)
        if password == confirm_password:
            return confirm_password
        else:
            print("Passwords do not match. Please try again.")

def check_mobile(message):
    regex = r'^01[0125][0-9]{8}$'
    while True:
        mobile = input(message)
        if re.fullmatch(regex, mobile):
            return mobile
        else:
            print("Please Enter a valid phone number.")

def save_to_file(user_data):
    # Insert the user information into the database
    c.execute("INSERT INTO users (name, last_name, email, password, mobile) VALUES (?, ?, ?, ?, ?)",
              (user_data['name'], user_data['last_name'], user_data['email'], user_data['password'], user_data['mobile']))
    conn.commit()

    print("User created successfully.")

def find_user(email, password):
    # Retrieve the user information for the given email and password from the database
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    if user:
        return True, user[0]
    else:
        return False, None

def valid_date(message="Please Enter a valid date (YYYY-MM-DD): "):
    while True:
        date_str = input(message)
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.date()
        except ValueError:
            print("Please Enter a valid date in the format YYYY-MM-DD.")

def generate_id():
    return round(time.time() * 1000)