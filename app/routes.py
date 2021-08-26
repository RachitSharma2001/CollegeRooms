from flask import render_template, redirect, request, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_sqlalchemy import event
from app import socketio, app, db
from app.forms import LoginForm, SignupForm, MessageForm
from app.models import Users, Message
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


@app.route('/logout')
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    # Add something to only show if user logs in
    logout_user()
    return render_template("logout.html")

@app.route('/suggestions')
@login_required
def suggestions():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    
    return "Suggestions"

@app.route('/pending_invites')
@login_required
def pending_invites():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    
    return "Invites"

@app.route('/message_room', methods=["GET", "POST"])
@login_required
def message():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    
    message_form = MessageForm()
    #event.listen(Message, "after_insert", render_template("room.html", messages=Users.query.get(current_user.id).messages, form=message_form))
    
    if message_form.validate_on_submit():
        user_from_id = current_user.id
        # Hard coded for now
        user_to_id = 2
        message_content = message_form.data['message']
        
        new_message = Message(user_from_id=user_from_id, user_to_id=user_to_id, content=message_content)
        db.session.add(new_message)
        db.session.commit()
        
        socketio.emit(str(user_to_id), {'new_message', new_message})
        # socket io emit new_message : content 
        # then in javascript of room, we can add something listens for this new message and loads the new messages
    
    return render_template("room.html", messages=Users.query.get(current_user.id).messages, form=message_form)

