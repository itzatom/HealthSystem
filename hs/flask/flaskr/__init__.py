from flask import Flask, request, render_template, Blueprint
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
import os
app = Flask(__name__)
app.secret_key = os.environ.get('SECRETKEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbahealthsystem:passwddba@postgres:5432/healthsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)



from .sql import models
from . import error_handler
from . import views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
