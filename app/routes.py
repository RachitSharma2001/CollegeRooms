from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import Users

@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # if the user is already logged in, redirect
        if current_user.is_authenticated:
            return redirect(url_for("message"))
        
        user = Users.query.filter_by(name=login_form.data['name']).first()
        if user is None or not user.check_password(login_form.data['password']):
            print("Incorrect password: ", login_form.data['password'])
            print("User: ", user)
            print("Check password: ", user.check_password(login_form.data['password']))
            print("Check password hi: ", user.check_password("hi"))
            return redirect(url_for("login"))
        
        login_user(user)
        return redirect(url_for("message"))

    return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    signup = SignupForm()
    if signup.validate_on_submit():
        # Get specific data
        name = signup.data['name']
        major = signup.data['major']
        hall = signup.data['hall']
        password = signup.data['password']
        
        user = Users(name=name, major=major, hall=hall)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("login"))

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