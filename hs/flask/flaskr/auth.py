from flaskr import app
from flask import render_template
from flask import request
from .sql.db import Session
from .sql.models import Persona

@app.route('/hs/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db_session = Session()
        utente = db_session.query(Persona.nome).all()
        return str(utente)
    else:
        return "<h1> ciao </h1>"
