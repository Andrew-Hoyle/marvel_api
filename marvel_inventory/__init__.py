from flask import Flask, config
from config import Config
from forms import forms
from helpers import helpers
from app import app
from routes import routes
from models import db as root_db, login_manager, ma
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from helpers import JSONEncoder

from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(config)

root_db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'templates.shared_templates.signin'

app.json_encoder = JSONEncoder