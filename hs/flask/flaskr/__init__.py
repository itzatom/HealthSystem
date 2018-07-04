from flask import Flask, request
from .db.db import engine, db_session
from .db.models import Persona

app = Flask(__name__)

@app.route("/hs", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        test = db_session.query(Persona.nome).all() 
        return "<h3> QUERIES FROM POSTGRES </h3>" + str(test)
    else:
        return "<h1> no POST method </h1>"
