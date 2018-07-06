from flaskr import app
from flask import render_template
from flask import request
from .sql.db_config import db
from .sql.models import Persona
from .sql.models import Medico
from .sql.models import StudLeg

@app.route('/hs/login', methods=['POST'])
def login():
    inp_username = request.form['form-username']
    inp_password = request.form['form-password']
    user = Persona.query.filter_by(username=inp_username).first()
    
    if user is not None:
        if user.check_password(inp_password):
            doctor = Medico.query.filter_by(id_medico=user.id_persona).first()
            
            if doctor is not None:
                return 'You are a doctor. You work from {0} to {1}'.format(doctor.stud_leg.da_giorno, doctor.stud_leg.a_giorno)
            else:
                return 'You are a patient.'
        
        else:
            return 'Access denied!'
    else:
        return 'User not found!'
