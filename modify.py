import sqlite3
from validate import check_string, valid_date, check_int

# Connect to the database
conn = sqlite3.connect('projects.db')
c = conn.cursor()

# Create the projects table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS projects
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              details TEXT,
              target INTEGER,
              start_date TEXT,
              end_date TEXT,
              user_id INTEGER)''')
conn.commit()

def create_project(user):
    # Prompt the user for project information
    title = check_string("Please Enter the project title: ")
    details = check_string("Please Enter the project details: ")
    target = check_int("Please Enter the project target: ")
    start_date = valid_date("Please Enter the project start date (YYYY-MM-DD): ")
    end_date = valid_date("Please Enter the project end date (YYYY-MM-DD): ")

    # Insert the project information into the database
    c.execute("INSERT INTO projects (title, details, target, start_date, end_date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
              (title, details, target, start_date, end_date, user))
    conn.commit()

    print("Project Created Successfully.")

def view_project(user_id):
    # Retrieve the projects for the given user ID from the database
    c.execute("SELECT * FROM projects WHERE user_id=?", (user_id,))
    projects = c.fetchall()

    # Print the project information
    for project in projects:
        print(project)

    return projects

def edit_project(user):
    # Retrieve all projects for the given user ID from the database
    all_projects = view_project(user)

    # Prompt the user to select a project to edit
    project_name = input('\nSelect one project to edit: ')

    for project in all_projects:
        if project[1] == project_name:
            # Prompt the user for the field to edit and the new value
            field = input('Select a field to edit (title/details/target/start_date/end_date): ')
            new_value = input('Enter the new value: ')

            # Update the project information in the database
            c.execute(f"UPDATE projects SET {field}=? WHERE id=?", (new_value, project[0]))
            conn.commit()

            print("Project updated successfully.")
            break
    else:
        print("Project not found.")

def delete_project(user):
    # Retrieve all projects for the given user ID from the database
    all_projects = view_project(user)

    # Prompt the user to select a project to delete
    project_name = input('\nSelect one project to delete: ')

    for project in all_projects:
        if project[1] == project_name:
            # Delete the project from the database
            c.execute("DELETE FROM projects WHERE id=?", (project[0],))
            conn.commit()

            print("Project deleted successfully.")
            break
    else:
        print("Project not found.")

def search(user_id):
    # Prompt the user for a date to search for
    project_date = valid_date("Please Enter the project date to search for (YYYY-MM-DD): ")

    # Retrieve the projects for the given user ID and date from the database
    c.execute("SELECT * FROM projects WHERE user_id=? AND start_date=? OR end_date=?", (user_id, project_date, project_date))
    projects = c.fetchall()

    # Print the project information
    for project in projects:
        print(project)