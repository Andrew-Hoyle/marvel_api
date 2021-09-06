from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin, login_manager


from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = login_manager.LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# USER CLASS

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), nullable = True, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'user {self.email} has been added to the database'



class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    powers = db.Column(db.String(250), nullable = False)
    first_issue = db.Column(db.String(50), nullable = True)
    secret_identity = db.Column(db.String(100), nullable = True)
    movie = db.Column(db.String(500), nullable = True)
    portrayed_by = db.Column(db.String(200), nullable = True)
    user_token = db.Column(db.ForeignKey('user.token'), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default= datetime.utcnow)

    def __init__(self,name,powers,first_issue,secret_identity,movie,portrayed_by,user_token,date_created,id='',):
        self.id = self.set_id()
        self.name = name
        self.powers = powers
        self.first_issues = first_issue
        self.secret_identity = secret_identity
        self.movie = movie
        self.portrayed_by = portrayed_by
        self.user_token = user_token


    def __repr__(self):
        return f'The following Drone has been added: {self.name}'
    
    def set_id(self):
        return secrets.token_urlsafe

class HeroSchema(ma.Schema):
    class Meta:
        field = ['id', 'name', 'powers', 'first_issues', 'secret_identity', 'movie', 'portrayed_by', 'user_token']

Hero_schema = HeroSchema()
Heros_schema = HeroSchema(many=True)


    


