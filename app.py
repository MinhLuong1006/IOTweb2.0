import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iotproject'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your mail provider if different
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'minhluong10062006@gmail.com'  # Change to your email
app.config['MAIL_PASSWORD'] = 'pclg gmfq phec uits'  # Use the App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'minhluong10062006@gmail.com'

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Token serializer

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Define user file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
USER_FILE = os.path.join(BASE_DIR, "users.txt")  # Ensure users.txt is in the same folder

# Function to save a new user to users.txt
def save_user(username, email, password):
    with open(USER_FILE, "a") as file:  # Open in append mode
        file.write(f"{username}, {email}, {password}\n")

# Function to load users from the file into a dictionary
def load_users():
    users = {}
    emails = {}
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
users, emails = load_users()

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:  # Check if user exists
        return User(user_id)
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Ensure passwords match
        if password != confirm_password:
            return "Passwords do not match, please try again."

        # Reload users to check if username is taken
        global users, emails
        users, emails = load_users()

        if username in users:
            return "Username already exists, please choose another one."

        # Save new user to file
        save_user(username, email, password)

        # Reload users after adding a new one
        users, emails = load_users()

        return redirect(url_for("login"))  # Redirect to login page after registration

    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Reload users before login attempt
        global users
        users, emails = load_users()

        if username in users and users[username] == password:
            user = User(username)
            login_user(user)  # Log in the user
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."

    return render_template('login.html', error=error)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Reset Password Feature
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']

        global users, emails
        users, emails = load_users()

        # Find username by email
        username = None
        for user, user_email in emails.items():
            if user_email == email:
                username = user
                break

        if not username:
            return "Email not found. Please try again."

        # Generate password reset token
        token = s.dumps(email, salt='password-reset')

        # Create reset URL
        reset_url = url_for('reset_with_token', token=token, _external=True)

        # Send email
        msg = Message("Password Reset Request", recipients=[email])
        msg.body = f"Click the link to reset your password: {reset_url}"
        mail.send(msg)

        return "Password reset link sent to your email."

    return render_template('reset_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt="password-reset", max_age=3600)  # Valid for 1 hour
    except SignatureExpired:
        return "The token is expired! Please request a new one."

    global users, emails
    users, emails = load_users()

    # Find username by email
    username = None
    for user, user_email in emails.items():
        if user_email == email:
            username = user
            break

    if not username:
        return "Invalid token!"

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            return "Passwords do not match, please try again."

        # Update password in users.txt
        updated_lines = []
        with open(USER_FILE, "r") as file:
            for line in file:
                user_data = line.strip().split(", ")
                if user_data[0] == username:  # Match username
                    updated_lines.append(f"{username}, {email}, {new_password}\n")
                else:
                    updated_lines.append(line)

        with open(USER_FILE, "w") as file:
            file.writelines(updated_lines)

        return redirect(url_for("login"))

    return render_template("reset_with_token.html")

# Keep all your room and building routes
@app.route('/building1')
@login_required
def building1():
    return render_template("building1.html")

@app.route('/building2')
@login_required
def building2():
    return render_template("building2.html")

@app.route('/room1')
@login_required
def room1():
    return render_template("room1.html")

@app.route('/room2')
@login_required
def room2():
    return render_template("room2.html")

@app.route('/room3')
@login_required
def room3():
    return render_template("room3.html")

@app.route('/room4')
@login_required
def room4():
    return render_template("room4.html")

@app.route('/event_log')
def event_log():
    return render_template('event_log.html')
if __name__ == '__main__':
    app.run(debug=True)
