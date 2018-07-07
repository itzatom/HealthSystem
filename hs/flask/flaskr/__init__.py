from flask import Flask, request, render_template, Blueprint
from .sql.db_config import db

app = Flask(__name__)

from . import error_handler
from . import views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
