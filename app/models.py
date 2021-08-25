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
    messages_received = db.relationship('Message', lazy='dynamic', foreign_keys='Message.user_to_id')
    messages_sent = db.relationship('Message', lazy='dynamic', foreign_keys='Message.user_from_id')

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
        return 'Message from {}, to {}, with content {}'.format(self.name)
    
    #def __lt__(self):
        
@login.user_loader
def load_user(id):
    return Users.query.get(int(id))