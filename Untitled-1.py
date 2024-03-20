<!DOCTYPE html>
<html>
<head>
	<title>Student Election System</title>
</head>
<body>
	<h1>Welcome to the Student Election System!</h1>
	<form action="/vote" method="post">
		<label for="candidate">Choose a candidate:</label>
		<select name="candidate">
			<option value="candidate1">Candidate 1</option>
			<option value="candidate2">Candidate 2</option>
			<option value="candidate3">Candidate 3</option>
		</select>
		<button type="submit">Vote</button>
	</form>
</body>
</html>
body {
	background-color: #f0f0f0;
	font-family: Arial, sans-serif;
}

h1 {
	color: #005a9c;
	text-align: center;
	margin-top: 50px;
}

form {
	background-color: #fff;
	padding: 20px;
	border-radius: 5px;
	box-shadow: 0px 0px 5px #ccc;
	margin: 50px auto;
	width: 5
 from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import sqlite3

app = Flask(_name_)
app.config['SECRET_KEY'] = 'mysecretkey'

# Setup database
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Create database if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                voter_id TEXT NOT NULL,
                is_voted BOOLEAN NOT NULL,
                is_registered BOOLEAN NOT NULL
                )''')

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define login routes
@login_manager.user_loader
def user_loader(user_id):
    c.execute("SELECT * FROM students WHERE id = ?", (user_id,))
    user = c.fetchone()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        voter_id = request.form['voter_id']
        c.execute("SELECT * FROM students WHERE voter_id = ?", (voter_id,))
        user = c.fetchone()

        if user and user['is_registered'] and not user['is_voted']:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid voter ID or you have already voted")
    return render_template('login.html')

@app.route('/logout')
@login