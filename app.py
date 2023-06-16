from flask import Flask, render_template, session, redirect, request, flash, url_for, jsonify
import sqlite3
import secrets
from datetime import datetime
from math import ceil


app = Flask(__name__)

# Generate a random secret key
secret_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string

# Set the secret key for the session
app.secret_key = secret_key

# Route for Home page

@app.route("/")
def home():
    # Set the title for the home page
    title = 'Home'
    # Render the 'index.html' template with the title variable
    return render_template('index.html', title=title)

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform user authentication
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Execute a query to check the username and password
        query = "SELECT * FROM Users WHERE UserName = ? AND Password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # If authentication is successful, store user data in the session
            session['username'] = user[0]  # Assuming the username is in the first column
            session['logged_in'] = True
            conn.close()
            return redirect('/dashboard')

        # Authentication failed, show error message
        error_message = 'Invalid username or password'
        conn.close()
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')


# Route for registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the registration form
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Check if the username is already taken
        query = "SELECT * FROM Users WHERE UserName = ?"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Username is already taken, show error message
            error_message = 'Username already taken'
            conn.close()
            return render_template('register.html', error_message=error_message)

        # Insert new user into the database
        query = "INSERT INTO Users (UserName, Password) VALUES (?, ?)"
        cursor.execute(query, (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# Route for dashboard page
@app.route("/dashboard")
def dashboard():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    else:
        # User is not logged in, redirect to login page
        return redirect('/login')


# Route for ToDo page
@app.route("/todo", methods=["GET", "POST"])
def todo():
    # Check if the user is logged in
    if session.get('logged_in'):
        # Get the username from the session
        username = session.get('username')

        # Connect to the SQLite database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Get the page number from the query parameters
        page = request.args.get('page', 1, type=int)
        rows_per_page = 6

        # Calculate the offset for pagination
        offset = (page - 1) * rows_per_page

        # Execute the SQL query to retrieve todo items for the logged-in user with pagination
        cursor.execute('SELECT * FROM todo WHERE UserName = ? LIMIT ? OFFSET ?',
                       (username, rows_per_page, offset))
        rows = cursor.fetchall()

        # Count the total number of rows for the logged-in user
        cursor.execute('SELECT COUNT(*) FROM todo WHERE UserName = ?', (username,))
        total_rows = cursor.fetchone()[0]

        # Calculate the total number of pages based on the total rows and rows per page
        total_pages = ceil(total_rows / rows_per_page)

        # Close the database connection
        conn.close()

        if request.method == "POST":
            # Get the form data
            title = request.form.get("todotitle")
            description = request.form.get("tododesc")
            date = datetime.now().strftime("%Y-%m-%d")

            # Connect to the SQLite database
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()

            # Execute the SQL query to insert the new task into the todo table
            cursor.execute('INSERT INTO todo (UserName, title, Description, Date) VALUES (?, ?, ?, ?)',
                           (username, title, description, date))
            conn.commit()

            # Close the database connection
            conn.close()

            flash("Task added successfully", "success")

            # Redirect to the ToDo page with the current page number
            return redirect(url_for('todo', page=page))

        # Render the template and pass the username, rows, total_pages, and current page to it
        return render_template('todo.html', username=username, rows=rows, total_pages=total_pages, page=page)

    else:
        # User is not logged in, redirect to the login page
        return redirect('/login')


# Route for marking a task as done
@app.route('/mark_done/<int:task_id>', methods=['POST'])
def mark_done(task_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('static/DB/Project_Management_System.db')
    cursor = conn.cursor()

    # Update the task status as done in the database
    cursor.execute('UPDATE todo SET Status = ? WHERE ID = ?', ('Done', task_id))
    conn.commit()

    # Close the database connection
    conn.close()

    # Return a JSON response indicating success
    return jsonify({'success': True})



# Route for deleting a task
@app.route('/delete_task', methods=['POST'])
def delete_task():
    # Get the task ID from the request form data
    task_id = request.form.get('task_id')

    # Connect to the SQLite database
    conn = sqlite3.connect('static/DB/Project_Management_System.db')
    cursor = conn.cursor()

    # Delete the task from the database
    cursor.execute('DELETE FROM todo WHERE id = ?', (task_id,))
    conn.commit()

    # Close the database connection
    conn.close()

    # Return a JSON response indicating success
    return jsonify({'success': True})

# Route for changing password
@app.route("/changepasswd", methods=['GET', 'POST'])
def changepassword():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')

        if request.method == 'POST':
            # Get the new password from the form
            new_password = request.form['password']

            # Update the password in the database
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute("UPDATE Users SET password = ? WHERE UserName = ?", (new_password, username))
                conn.commit()
                flash("Password changed successfully!", "success")
            except Exception as e:
                flash("An error occurred. Please try again later.", "danger")
                print(e)
            finally:
                conn.close()

            return redirect('/changepasswd')  # Redirect to the same page after updating the password

        return render_template('passwd.html', username=username)

    else:
        # User is not logged in, redirect to login page
        return redirect('/login')


# Route for logging out
@app.route("/logout")
def Logout():
    # Clear the session data
    session.clear()
    return redirect('/login')

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
