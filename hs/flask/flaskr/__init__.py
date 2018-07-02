from flask import Flask
from .db.db import engine, db_session
from .db.models import Persona

app = Flask(__name__)

@app.route ("/")
def index():
    test = db_session.query(Persona.nome).all() 
    return str(test) 

if __name__ == "__main__":
    app.run(port=5000)
