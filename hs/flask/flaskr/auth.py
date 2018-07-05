from flaskr import app, render_template, request
from .sql.db import Session
from .sql.models import Persona
from flask_sqlalchemy import SQLAlchemy

@app.route('/hs/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db_session = Session()
        username = db_session.query(Persona).select_from(Persona).filter(Persona.username == request.form['form-username'])
        return username
    else:
        return "<h1> ciao </h1>"
