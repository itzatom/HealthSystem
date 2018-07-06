from flask import Flask, request, render_template
from .sql.db_config import db

app = Flask(__name__)

from . import auth

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

