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
conn.close()
