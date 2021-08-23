from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    major = db.Column(db.String(100))
    hall = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, given_password):
        return check_password_hash(self.password, given_password)

    def __repr__(self):
        return 'User {}'.format(self.name)
    
@login.user_loader
def load_user(id):
    return Users.query.get(int(id))