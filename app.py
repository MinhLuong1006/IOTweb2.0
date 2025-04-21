import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iotproject'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'minhluong10062006@gmail.com'  
app.config['MAIL_PASSWORD'] = 'pclg gmfq phec uits'  # App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'minhluong10062006@gmail.com'

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Token serializer

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'minhluong10062006@gmail.com'  
app.config['MAIL_PASSWORD'] = 'pclg gmfq phec uits'  # App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'minhluong10062006@gmail.com'

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Token serializer

=======
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import firebase_admin
from firebase_admin import credentials, db
import time
from flask_cors import CORS
import bcrypt
import threading



last_email_time = 0
COOLDOWN_PERIOD = 180

last_alarm_state1 = 0
last_alarm_state2 = 0
last_alarm_state3 = 0
last_alarm_state4 = 0

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Initialize Firebase Admin SDK
cred = credentials.Certificate("esp32-fire-alarm-a8fc5-firebase-adminsdk-fbsvc-7af4c28f95.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://esp32-fire-alarm-a8fc5-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

app.config['SECRET_KEY'] = 'iotproject'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'minhluong10062006@gmail.com'  
app.config['MAIL_PASSWORD'] = 'pclg gmfq phec uits'  # App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = ('FireAlarm', 'minhluong10062006@gmail.com')

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Token serializer

>>>>>>> Stashed changes
# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Define user file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
USER_FILE = os.path.join(BASE_DIR, "users.txt")  # Ensure users.txt is in the same folder

# Function to save a new user to users.txt
def save_user(username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with open(USER_FILE, "a") as file:  # Open in append mode
        file.write(f"{username}, {email}, {hashed_password}, user\n")

# Function to load users from the file into a dictionary
def load_users():
    users = {}
    if os.path.exists(USER_FILE):  # Ensure the file exists
        with open(USER_FILE, "r") as file:
            for line in file:
                try:
                    username, email, password = line.strip().split(", ")
                    users[username] = password  # Store username-password in dictionary
                    emails[username] = email  # Store username-email mapping
                except ValueError:
                    continue  # Skip malformed lines
    return users, emails

# Load users into memory
users = load_users()

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:  # Check if user exists
        return User(user_id)
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
     error = None

     if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 1. Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match, please try again."
            return render_template('auth/register.html', error=error)

<<<<<<< Updated upstream
        # Reload users to check if username is taken
        global users
        users = load_users()

        if username in users:
            error = "Username already exists, please choose another one."
            return render_template('auth/register.html', error=error)

        # 3. Save new user (with default role "user")
        save_user(username, email, password)

<<<<<<< Updated upstream
        # Reload users after adding a new one
        users = load_users()

        return redirect(url_for("login"))

     return render_template('auth/register.html', error=error)


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

<<<<<<< Updated upstream
        # Reload users before login attempt
        global users
        users = load_users()

        if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8')):
            user = User(username)
            login_user(user)

            # Store user info in session
            session["username"] = username
            session["role"] = roles.get(username, "user")  # Default to 'user' if missing

            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."

    return render_template('auth/login.html', error=error)

<<<<<<< Updated upstream
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/building1')
@login_required
def building1():
    return render_template("buildings/building1.html")

@app.route('/building2')
@login_required
def building2():
    return render_template("buildings/building2.html")

@app.route('/room1')
@login_required
def room1():
    return render_template("rooms/room1.html")

@app.route('/room2')
@login_required
def room2():
    return render_template("rooms/room2.html")

@app.route('/room3')
@login_required
def room3():
    return render_template("rooms/room3.html")

@app.route('/room4')
@login_required
def room4():
    return render_template("rooms/room4.html")
if __name__ == '__main__':
    app.run(debug=True)
