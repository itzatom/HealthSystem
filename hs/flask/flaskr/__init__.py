from flask import Flask, request, render_template
from .sql.db import engine, Session

app = Flask(__name__)

from . import auth

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

