from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    major = db.Column(db.String(100))
    hall = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __repr__(self):
        return 'User {}'.format(self.name)