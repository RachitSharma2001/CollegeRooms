from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import or_

# Database table to store all the users
class Users(UserMixin, db.Model):
    #### Define key table entries ####
    NAME_SIZE = 100
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_SIZE), unique=True)
    major = db.Column(db.String(100))
    hall = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # Table entry to store all messages either to user or from user
    messages = db.relationship('Message', lazy='dynamic', primaryjoin="or_(Users.id == Message.user_to_id, Users.id == Message.user_from_id)")

    ##### Defining key functions ####

    # Gives all messages from current_user to friend
    def giveMessagesFrom(current_user_id, friend_id):
        return Users.query.get(current_user_id).messages.filter(or_(Message.user_to_id==friend_id, Message.user_from_id==friend_id))

    # Sets password of current User
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    # Check password attempt by current user
    def check_password(self, given_password):
        return check_password_hash(self.password, given_password)

    # Print representation of Users
    def __repr__(self):
        return 'User {}'.format(self.name)

# Database table store all the messages between users
class Message(db.Model):
    #### Define key table entries ####
    MAX_CHARS_IN_MESSAGE = 1000
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(MAX_CHARS_IN_MESSAGE))
    
    ##### Defining key functions ####
    
    # Gives the name of User who sent message
    def give_name(self, user_id):
        name = "You"
        if not (self.user_from_id == user_id):
            name = Users.query.get(self.user_from_id).name
        
        return name
    
    # Print representation of Users
    def __repr__(self):
        return 'Given_Message from {} to {}, with content: {}'.format(self.user_from_id, self.user_to_id, self.content)

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))