from flaskr import app
from flaskr import login_manager
from flask import url_for, session, redirect, request, render_template, flash
from flask_login import login_user, login_required, logout_user
from .sql.models import Persona
from .sql.models import Medico

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/hs/login', methods=['GET', 'POST'])
def login():
    inp_username = request.form['form-username']
    inp_password = request.form['form-password']
    user = Persona.query.filter_by(username=inp_username).first()

    if user is not None and user.check_password(inp_password):
        login_user(user)
        doctor = Medico.query.filter_by(id_medico=user.id_persona).first()

        if doctor is not None:
            return redirect(request.args.get('next') or url_for('doctor', Persona=user))
        else:
            return redirect(url_for('patient', Persona=user))

    flash('Invalid username or password.')
    return render_template('index.html')

@app.route('/hs/doctor/<Persona>', methods=['GET','POST'])
@login_required
def doctor(Persona):
    if request.method == 'GET':
        return render_template('homepage/doctor.html');

@app.route('/hs/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/hs/patient/<Persona>', methods=['GET','POST'])
@login_required
def patient(Persona):
    if request.method == 'GET':
        return render_template('homepage/patient.html');
