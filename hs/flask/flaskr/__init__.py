from flask import Flask, request, render_template
from .db.db import engine, db_session
from .db.models import Persona
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/main", methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        test = db_session.query(Persona.nome).all() 
        return "<h3> QUERIES FROM POSTGRES </h3>" + str(test)
    else:
        return "<h1> no POST method </h1>"
