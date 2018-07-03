from flask import Flask
from .db.db import engine, db_session
from .db.models import Persona

app = Flask(__name__)

@app.route("/nginxflask", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        test = db_session.query(Persona.nome).all() 
        return str(test) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
