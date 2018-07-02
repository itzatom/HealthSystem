import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Persona
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_MED_URL')
db = SQLAlchemy(app)


@app.route ("/")
def index():
    test = db.session.query(Persona).all()
    return test
if __name__ == "__main__":
    app.run()
