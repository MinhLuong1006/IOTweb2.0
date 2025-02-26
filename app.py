from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iotproject'

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Manually stored users (username: password)
users = {
    "khangyeuloli25072006": "Toicodon1",
    "hoangyeuyoungboi11506": "234",
    "Khiemlol": "029",
    "minhbell": "10062006",
    "DonutdaddyTriTran2006": "Chocolatespecial25",
    "Ducanhngo": "12345678"

}

# User model for Flask-Login (not using a database)
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

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            user = User(username)
            login_user(user)  # Log in the user
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
