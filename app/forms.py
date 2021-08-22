from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired 

class SignupForm(FlaskForm):
    name = StringField("Enter name", [DataRequired()])
    major = StringField("Enter Major", [DataRequired()])
    # Make this a dropdown of all halls
    hall = StringField("Enter hall", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    signup = SubmitField("Sign up!")

class LoginForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    login = SubmitField("Login")