import sqlite3

# Connect to the database (creates a new database if it doesn't exist)
conn = sqlite3.connect('Project_Management_System.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Create a  Users table

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserName TEXT,
        Password TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
print("User Table Created Sucessfully!")

#  Create ToDo table

cursor.execute('''
    CREATE TABLE IF NOT EXISTS todo (
        "TaskID"	INTEGER,
	    "UserName"	TEXT,
	    "Title"	TEXT,
	    "Description"	TEXT,
	    "Date"	NUMERIC,
	    "Done"	INTEGER DEFAULT 0,
	    "Status"	TEXT,
	    PRIMARY KEY("TaskID" AUTOINCREMENT)
     )''')

# Commit the changes and close the connection
conn.commit()
print("ToDo Table Created Sucessfully!")

# Create Project table
cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT,UserName Text, name TEXT, description TEXT)")
conn.commit()
print("Project Table Created Sucessfully!")

# Create Tasks table
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, taskName TEXT, taskDesc TEXT)")
conn.commit()
print("Tasks Table Created Successfully!")

# Create Teams table
cursor.execute("CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, teamName TEXT, teamDesc TEXT, teamMembers TEXT)")
conn.commit()
print("Teams Table Created Successfully!")






conn.close()
