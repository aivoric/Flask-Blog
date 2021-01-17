'''
All the database models are contained here:
- Users
- Blog Posts
'''

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    '''
    Defines the user model for the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        '''Turns a password string into a hash.'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Converts password into a hash, and then checks against stored hash.'''
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    '''
    Blog post database model. It has a relationship to the user.
    Each user can have many blog posts.
    '''
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)

@login.user_loader
def load_user(id):
    '''Flask login extensions uses user IDs. This helper function helps retrieve
    the user based on their id.'''
    return User.query.get(int(id))
