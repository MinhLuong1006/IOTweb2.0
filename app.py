import os
<<<<<<< Updated upstream
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iotproject'

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
<<<<<<< Updated upstream
    if os.path.exists(USER_FILE):  # Ensure the file exists
        with open(USER_FILE, "r") as file:
            for line in file:
                try:
                    username, email, password = line.strip().split(", ")
                    users[username] = password  # Store username-password in dictionary
                except ValueError:
                    continue  # Skip malformed lines
    return users

# Load users into memory
users = load_users()
=======
    emails = {}
    roles = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            for line in file:
                try:
                    parts = line.strip().split(", ")
                    if len(parts) >= 3:
                        username, email, password = parts[0], parts[1], parts[2]
                        role = parts[3] if len(parts) >= 4 else "user"
                        users[username] = password
                        emails[username] = email
                        roles[username] = role
                except ValueError:
                    continue  # Skip malformed lines
    return users, emails, roles

# Load users into memory
users, emails, roles = load_users()
>>>>>>> Stashed changes

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
=======
        # 2. Reload users to check if username is already taken
        global users, emails, roles
        users, emails, roles = load_users()
>>>>>>> Stashed changes

        if username in users:
            error = "Username already exists, please choose another one."
            return render_template('auth/register.html', error=error)

        # 3. Save new user (with default role "user")
        save_user(username, email, password)

<<<<<<< Updated upstream
        # Reload users after adding a new one
        users = load_users()
=======
        # 4. Reload users to update memory
        users, emails, roles = load_users()
>>>>>>> Stashed changes

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
=======
        global users, emails, roles
        users, emails, roles = load_users()
>>>>>>> Stashed changes

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
=======

>>>>>>> Stashed changes

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

<<<<<<< Updated upstream
=======
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

    return render_template('auth/reset_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt="password-reset", max_age=3600)  # Valid for 1 hour
    except SignatureExpired:
        return "The token is expired! Please request a new one."

    global users, emails
    users, emails, roles = load_users()

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
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        updated_lines = []
        with open(USER_FILE, "r") as file:
            for line in file:
                user_data = line.strip().split(", ")
                if user_data[0] == username:  # Match username
                    updated_lines.append(f"{username}, {email}, {hashed_password}\n")
                else:
                    updated_lines.append(line)

        with open(USER_FILE, "w") as file:
            file.writelines(updated_lines)

        return redirect(url_for("login"))

    return render_template("auth/reset_with_token.html")

@app.route('/user_panel')
@login_required
def user_panel():
    # Only allow admin
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))  # Or return a 403 error

    global users, emails
    users, emails, _ = load_users()

    user_list = [{"username": u, "email": emails[u]} for u in users if u != session.get("username")]

    return render_template("admin/user_panel.html", users=user_list)

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))

    username_to_delete = request.form.get("username")

    # Prevent admin from deleting themselves
    if username_to_delete == session.get("username"):
        return redirect(url_for("user_panel"))

    lines = []
    with open(USER_FILE, "r") as file:
        lines = file.readlines()
    with open(USER_FILE, "w") as file:
        for line in lines:
            if not line.startswith(username_to_delete + ","):
                file.write(line)

    # Reload users after deletion
    global users, emails, roles
    users, emails, roles = load_users()

    return redirect(url_for("user_panel"))

@app.route("/admin/control", methods=["GET", "POST"])
@login_required
def admin_control():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))  # Only allow admin

    alarm_ref = db.reference("/")

    if request.method == "POST":
        for i in range(1, 5):
            manu_room = f"alarm{i}_manu"
            real_room = f"alarm{i}"
            new_value = request.form.get(manu_room)

            if new_value in ["0", "1", "-1"]:
                int_val = int(new_value)
                alarm_ref.child(manu_room).set(int_val)

                # `alarm1_mannu` can be controlled by the admin, but doesn't affect `alarm1` anymore
                # So, `alarm1` remains controlled by the sensors
                # `alarm1_mannu` will store the manual override value for reference

        return redirect(url_for("admin_control"))

    # Get the current status of alarms
    current_status = {}
    for i in range(1, 5):
        current_status[f"alarm{i}"] = alarm_ref.child(f"alarm{i}").get() or 0
        current_status[f"alarm{i}_manu"] = alarm_ref.child(f"alarm{i}_manu").get() or 0

    return render_template("admin/control_panel.html", status=current_status)

# rooms and buildings routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("features/dashboard.html", username=current_user.id)

>>>>>>> Stashed changes
@app.route('/building1')
@login_required
def building1():
    return render_template("building/building1.html")

@app.route('/building2')
@login_required
def building2():
    return render_template("building/building2.html")


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
<<<<<<< Updated upstream
=======

@app.route('/event_log')
def event_log():
    return render_template('features/event_log.html')

@app.route('/event_log_b1')
def event_log_b1():
    return render_template('features/event_log_b1.html')

@app.route('/event_log_b2')
def event_log_b2():
    return render_template('features/event_log_b2.html')

@app.route('/event_log_r1')
def event_log_r1():
    return render_template('features/event_log_r1.html')

@app.route('/event_log_r2')
def event_log_r2():
    return render_template('features/event_log_r2.html')

@app.route('/event_log_r3')
def event_log_r3():
    return render_template('features/event_log_r3.html')

@app.route('/event_log_r4')
def event_log_r4():
    return render_template('features/event_log_r4.html')
###############################
def control_alarm1_logic():
    while True:
        # Fetch current values for alarm1, alarm1_mannu, and real_alarm1
        alarm1_manu = db.reference("alarm1_manu").get()
        alarm1_sensor = db.reference("alarm1_sensor").get()
        real_alarm1 = db.reference("real_alarm1").get()
        # Dynamically calculate real_alarm1 based on the logic you want
        if alarm1_manu == 1:
            # Force ON (manual override)
            real_alarm1 = 1
        elif alarm1_manu == -1:
            # Force OFF (manual override)
            real_alarm1 = 0
            db.reference("alarm1").set(0)
        else:
            # Neutral state (sensor controlled)
            if alarm1_sensor == 1:
                real_alarm1 = 1
        # Update real_alarm1 on Firebase in real-time  
        db.reference("real_alarm1").set(real_alarm1)

        # Sleep for a short time to avoid excessive reads/writes to Firebase
        time.sleep(2)

# Start the control thread
threading.Thread(target=control_alarm1_logic, daemon=True).start()
#CHECKALARM1
@app.route("/check_alarm1")
def check_alarm1():
    alarm1 = db.reference("/real_alarm1").get()
    return jsonify({"alarm1": alarm1})
# Function to send a fire alert email
def monitor_fire_room1():
    prev_alarm = 0  # To track previous alarm state (0 = no fire, 1 = fire)

    while True:
        alarm = db.reference("real_alarm1").get()

        # Fire just started
        if alarm == 1 and prev_alarm == 0:
            users, emails, roles = load_users()  # Load users and emails
            with app.app_context():  # Manually push the app context
                for username, email in emails.items():
                    send_fire_alert1(email)  # Send email to each user
                    print(f"🔥 Email sent to {email} for Room 1 fire")
            prev_alarm = 1

        # Fire put out
        elif alarm == 0:
            prev_alarm = 0

        time.sleep(3)  # Check every 5 seconds

# Start background monitoring
threading.Thread(target=monitor_fire_room1, daemon=True).start()
# Function to send a fire alert email

def send_fire_alert1(email):
    msg = Message("🔥 Room1 Fire Alert!", recipients=[email])
    msg.body = "Fire detected in Room 1! Please check immediately."
    mail.send(msg)

#################################################################
def control_alarm2_logic():
    while True:
        # Fetch current values for alarm1, alarm1_mannu, and real_alarm1
        alarm2_manu = db.reference("alarm2_manu").get()
        alarm2_sensor = db.reference("alarm2_sensor").get()
        real_alarm2 = db.reference("real_alarm2").get()
        # Dynamically calculate real_alarm1 based on the logic you want
        if alarm2_manu == 1:
            # Force ON (manual override)
            real_alarm2 = 1
        elif alarm2_manu == -1:
            # Force OFF (manual override)
            real_alarm2 = 0
            db.reference("alarm2").set(0)
        else:
            # Neutral state (sensor controlled)
            if alarm2_sensor == 1:
                real_alarm2 = 1
        # Update real_alarm1 on Firebase in real-time  
        db.reference("real_alarm2").set(real_alarm2)

        # Sleep for a short time to avoid excessive reads/writes to Firebase
        time.sleep(2)

# Start the control thread
threading.Thread(target=control_alarm2_logic, daemon=True).start()
#CHECKALARM2
@app.route("/check_alarm2")
def check_alarm2():
    alarm2 = db.reference("/real_alarm2").get()
    return jsonify({"alarm2": alarm2})
# Function to send a fire alert email
def monitor_fire_room2():
    prev_alarm = 0  # To track previous alarm state (0 = no fire, 1 = fire)

    while True:
        alarm = db.reference("real_alarm2").get()

        # Fire just started
        if alarm == 1 and prev_alarm == 0:
            users, emails, roles = load_users()  # Load users and emails
            with app.app_context():  # Manually push the app context
                for username, email in emails.items():
                    send_fire_alert2(email)  # Send email to each user
                    print(f"🔥 Email sent to {email} for Room 2 fire")
            prev_alarm = 1

        # Fire put out
        elif alarm == 0:
            prev_alarm = 0

        time.sleep(3)  # Check every 5 seconds

# Start background monitoring
threading.Thread(target=monitor_fire_room2, daemon=True).start()
# Function to send a fire alert email
def send_fire_alert2(email):
    msg = Message("🔥 Room2 Fire Alert!", recipients=[email])
    msg.body = "Fire detected in Room 2! Please check immediately."
    mail.send(msg)

##################################################################
def control_alarm3_logic():
    while True:
        # Fetch current values for alarm1, alarm1_mannu, and real_alarm1
        alarm3_manu = db.reference("alarm3_manu").get()
        alarm3_sensor = db.reference("alarm3_sensor").get()
        real_alarm3 = db.reference("real_alarm3").get()
        # Dynamically calculate real_alarm1 based on the logic you want
        if alarm3_manu == 1:
            # Force ON (manual override)
            real_alarm3 = 1
        elif alarm3_manu == -1:
            # Force OFF (manual override)
            real_alarm3 = 0
            db.reference("alarm3").set(0)
        else:
            # Neutral state (sensor controlled)
            if alarm3_sensor == 1:
                real_alarm3 = 1
        # Update real_alarm1 on Firebase in real-time  
        db.reference("real_alarm3").set(real_alarm3)

        # Sleep for a short time to avoid excessive reads/writes to Firebase
        time.sleep(2)

# Start the control thread
threading.Thread(target=control_alarm3_logic, daemon=True).start()
#CHECKALARM2
@app.route("/check_alarm3")
def check_alarm3():
    alarm3 = db.reference("/real_alarm3").get()
    return jsonify({"alarm3": alarm3})
# Function to send a fire alert email
def monitor_fire_room3():
    prev_alarm = 0  # To track previous alarm state (0 = no fire, 1 = fire)

    while True:
        alarm = db.reference("real_alarm3").get()

        # Fire just started
        if alarm == 1 and prev_alarm == 0:
            users, emails, roles = load_users()  # Load users and emails
            with app.app_context():  # Manually push the app context
                for username, email in emails.items():
                    send_fire_alert3(email)  # Send email to each user
                    print(f"🔥 Email sent to {email} for Room 3 fire")
            prev_alarm = 1

        # Fire put out
        elif alarm == 0:
            prev_alarm = 0

        time.sleep(3)  # Check every 5 seconds

# Start background monitoring
threading.Thread(target=monitor_fire_room3, daemon=True).start()
# Function to send a fire alert email
def send_fire_alert3(email):
    msg = Message("🔥 Room3 Fire Alert!", recipients=[email])
    msg.body = "Fire detected in Room 3! Please check immediately."
    mail.send(msg)
#####################################################################

def control_alarm4_logic():
    while True:
        # Fetch current values for alarm1, alarm1_mannu, and real_alarm1
        alarm4_manu = db.reference("alarm4_manu").get()
        alarm4_sensor = db.reference("alarm4_sensor").get()
        real_alarm4 = db.reference("real_alarm4").get()
        # Dynamically calculate real_alarm1 based on the logic you want
        if alarm4_manu == 1:
            # Force ON (manual override)
            real_alarm4 = 1
        elif alarm4_manu == -1:
            # Force OFF (manual override)
            real_alarm4 = 0
            db.reference("alarm4").set(0)
        else:
            # Neutral state (sensor controlled)
            if alarm4_sensor == 1:
                real_alarm4 = 1
        # Update real_alarm1 on Firebase in real-time  
        db.reference("real_alarm4").set(real_alarm4)

        # Sleep for a short time to avoid excessive reads/writes to Firebase
        time.sleep(2)

# Start the control thread
threading.Thread(target=control_alarm4_logic, daemon=True).start()
#CHECKALARM2
@app.route("/check_alarm4")
def check_alarm4():
    alarm4 = db.reference("/real_alarm4").get()
    return jsonify({"alarm4": alarm4})
# Function to send a fire alert email
def monitor_fire_room4():
    prev_alarm = 0  # To track previous alarm state (0 = no fire, 1 = fire)

    while True:
        alarm = db.reference("real_alarm4").get()

        # Fire just started
        if alarm == 1 and prev_alarm == 0:
            users, emails, roles = load_users()  # Load users and emails
            with app.app_context():  # Manually push the app context
                for username, email in emails.items():
                    send_fire_alert4(email)  # Send email to each user
                    print(f"🔥 Email sent to {email} for Room 4 fire")
            prev_alarm = 1

        # Fire put out
        elif alarm == 0:
            prev_alarm = 0

        time.sleep(3)  # Check every 5 seconds

# Start background monitoring
threading.Thread(target=monitor_fire_room4, daemon=True).start()
# Function to send a fire alert email
def send_fire_alert4(email):
    msg = Message("🔥 Room4 Fire Alert!", recipients=[email])
    msg.body = "Fire detected in Room 4! Please check immediately."
    mail.send(msg)
    
>>>>>>> Stashed changes
if __name__ == '__main__':
    app.run(debug=True)
