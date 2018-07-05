from flask import Flask, request, render_template
from .sql.db import engine, Session

app = Flask(__name__)

<<<<<<< HEAD
from . import auth

=======
>>>>>>> 2b4bc278b9007272e00124e90a2a6842747c8fc2
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

