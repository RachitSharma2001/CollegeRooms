from app import app, db
from app.forms import LoginForm, SignupForm, MessageForm
from app.models import Users, Message
from flask import render_template, redirect, request, flash, jsonify, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_sqlalchemy import event
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    # if the user is already logged in, redirect
    if current_user.is_authenticated:
        return redirect(url_for("message"))
        
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Users.query.filter_by(name=login_form.data['name']).first()
        if user is None or not user.check_password(login_form.data['password']):
            return redirect(url_for("login"))
        
        login_user(user)
        
        next_page = request.args.get('next')
        # second argument needed for security purposes
        if not next_page or url_parse(next_page) != '':
            return redirect(url_for("message"))
        
        return redirect(next_page)

    return render_template("login.html", form=login_form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("message"))
    
    signup = SignupForm()
    if signup.validate_on_submit():
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

@app.route('/logout')
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    logout_user()
    return render_template("logout.html")

# URL routed to when user logs in and when user changes who to message
@app.route('/message_room', methods=["GET", "POST"])
@app.route('/message_room/<current_friend>', methods=["GET", "POST"])
@login_required
def message(current_friend=None):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    
    message_form = MessageForm(choices=current_user.id)
    
    # If user sends message to another user, add to database
    if message_form.validate_on_submit():
        user_from_id = current_user.id
        user_to_id = message_form.data['choices']
        message_content = message_form.data['message']
        
        new_message = Message(user_from_id=user_from_id, user_to_id=user_to_id, content=message_content)
        db.session.add(new_message)
        db.session.commit()

    if current_friend == None:
        # Show all messages if specific DM not selected
        return render_template("room.html", messages=Users.query.get(current_user.id).messages, form=message_form)
    else:
        # If specific user to DM is selected, rerender messages to show only that messages to/from that user
        message_form = MessageForm(choices=current_friend)
        return render_template("room.html", messages=Users.giveMessagesFrom(current_user.id, current_friend), form=message_form)
