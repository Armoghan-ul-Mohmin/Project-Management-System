from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # Set the title for the home page
    title = 'Home'
    # Render the 'index.html' template with the title variable
    return render_template('index.html', title=title)

# Run the Flask application in debug mode
app.run(debug=True)
