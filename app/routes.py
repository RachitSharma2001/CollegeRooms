from flask import render_template
from app import app
from app.forms import LoginForm, SignupForm

@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    return render_template("login.html", form=login_form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    signup = SignupForm()
    if signup.validate_on_submit():
        return "Validated"
    return render_template("signup.html", form=signup)

@app.route('/suggestions')
def suggestions():
    return "Suggestions"

@app.route('/pending_invites')
def pending_invites():
    return "Invites"

@app.route('/message_room')
def message():
    return "Message room"