from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app.models import Users
from app import app

class SignupForm(FlaskForm):
    name = StringField("Enter name", [DataRequired()])
    major = StringField("Enter major", [DataRequired()])
    # Make this a dropdown of all halls
    hall = StringField("Enter hall", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    signup = SubmitField("Sign up!")

class LoginForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    login = SubmitField("Login")

class ChoiceForm(FlaskForm):
    def returnAllUsers():
        users = []
        for user in Users.query.all():
            users.append((user.id, user.name))
        return users
    options = SelectField("To whom", choices=returnAllUsers(), render_kw={"onchange" : "test_function()"})

class MessageForm(FlaskForm):

    def returnAllUsers():
        users = []
        for user in Users.query.all():
            users.append((user.id, user.name))
        return users

    message = StringField("Enter Message", [DataRequired()])
    choices = SelectField("To whom", choices=returnAllUsers())
    send = SubmitField("Send")