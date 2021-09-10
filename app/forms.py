from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app.models import Users
from app import app

# Sign up form
class SignupForm(FlaskForm):
    name = StringField("Enter name", [DataRequired()])
    major = StringField("Enter major", [DataRequired()])
    hall = StringField("Enter hall", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    signup = SubmitField("Sign up!")

# Log in form
class LoginForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    login = SubmitField("Login")

# Form allowing user to send messages
class MessageForm(FlaskForm):

    def returnAllUsers():
        users = []
        for user in Users.query.all():
            users.append((user.id, user.name))
        return users
    
    message = StringField("Enter Message", [DataRequired()])
    # Field to select specific user to message; when its changed it calls javascript function in room.html
    choices = SelectField("To whom", choices=returnAllUsers(), render_kw={"onchange" : "test_function()"})
    send = SubmitField("Send", render_kw={"onchange" : "scroll_down()"})