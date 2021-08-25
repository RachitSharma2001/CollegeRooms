from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Users(UserMixin, db.Model):
    NAME_SIZE = 100
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_SIZE), unique=True)
    major = db.Column(db.String(100))
    hall = db.Column(db.String(100))
    password = db.Column(db.String(100))
    messages = db.relationship('Message', lazy='dynamic', primaryjoin="or_(Users.id == Message.user_to_id, Users.id == Message.user_from_id)")

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, given_password):
        return check_password_hash(self.password, given_password)

    def __repr__(self):
        return 'User {}'.format(self.name)

class Message(db.Model):
    MAX_CHARS_IN_MESSAGE = 1000
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(MAX_CHARS_IN_MESSAGE))
    
    def __repr__(self):
        return 'Given_Message from {} to {}, with content: {}'.format(self.user_from_id, self.user_to_id, self.content)
    
    def give_name(self, user_id):
        name = "You"
        if not (self.user_from_id == user_id):
            name = Users.query.get(self.user_from_id).name
        
        return name

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))