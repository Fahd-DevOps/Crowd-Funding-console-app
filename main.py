from validate import check_string, check_email, is_equal, check_mobile
from modify import create_project, view_project, delete_project, search, edit_project
import sqlite3

# Connect to the database
conn = sqlite3.connect('projects.db')
c = conn.cursor()


def register_user():
    """

    :rtype: object
    """
    first_name = check_string("Please enter your first name: ")
    last_name = check_string("Please enter your last name: ")
    email = check_email("Please enter your email address: ")

    # Check if the email is already registered
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()

    if user:
        print("This email is already registered. Please try again.")
    else:
        password = input("Please enter your password: ")
        confirm_password = is_equal(password, "Please confirm your password: ")
        mobile = check_mobile("Please enter your mobile number: ")
        user_data = (first_name, last_name, email, password, mobile)

        # Insert the user information into the database
        c.execute("INSERT INTO users (name, last_name, email, password, mobile) VALUES (?, ?, ?, ?, ?)", user_data)
        conn.commit()
        print("User created successfully.")


def login_user():
    email = check_email("Please enter your email address: ")
    password = input("Please enter your password: ")

    # Retrieve the user information for the given email and password from the database
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    if user:
        print("Welcome, " + user[1] + "!")
        while True:
            print("Please choose what you want to do:")
            print("n: Create a new project")
            print("v: View your projects")
            print("e: Edit a project")
            print("d: Delete a project")
            print("s: Search for a project")
            print("x: Exit")

            choice = input("Your choice: ")

            if choice == "n":
                create_project(user[0])
            elif choice == "v":
                view_project(user[0])
            elif choice == "e":
                edit_project(user[0])
            elif choice == "d":
                delete_project(user[0])
            elif choice == "s":
                search(user[0])
            elif choice == "x":
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Invalid email or password. Please try again.")


print("Welcome to our application.")

while True:
    choice = input("Please choose: r to register, l to login, or x to exit: ")

    if choice == "r":
        register_user()
    elif choice == "l":
        login_user()
    elif choice == "x":
        break
    else:
        print("Invalid option. Please try again.")
