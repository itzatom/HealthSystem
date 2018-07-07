from flaskr import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from .sql.db_config import db
from .sql.models import Persona
from .sql.models import Medico
from .sql.models import StudLeg

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/hs/login', methods=['POST'])
def login():
    inp_username = request.form['form-username']
    inp_password = request.form['form-password']
    user = Persona.query.filter_by(username=inp_username).first()

    if user is not None:
        if user.check_password(inp_password):
            doctor = Medico.query.filter_by(id_medico=user.id_persona).first()
            if doctor is not None:
                return redirect(url_for('doctor', name=user.nome))
            else:
                return 'You are a patient.'
        else:
            return 'Access denied!'
    else:
        return 'User not found!'

@app.route('/hs/doctor/<name>', methods=['GET','POST'])
def doctor(name):
    if request.method == 'GET':
        return render_template('homepage/doctor.html');
