from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

app = Flask(__name__)
app.secret_key = 'our secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbahealthsystem:passwddba@postgres:5432/healthsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from .sql import models
from . import error_handler
from . import views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
