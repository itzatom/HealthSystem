from flaskr import app, db
from flaskr import login_manager
from flask import url_for, session, redirect, request, render_template, flash
from flask_login import login_user, login_required, logout_user
from .sql.models import Persona
from .sql.models import Medico, Paziente, Ricetta
from datetime import date

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
            return redirect(request.args.get('next') or url_for('doctor', _username=doctor.persona.username))
        else:
            return redirect(request.args.get('next') or url_for('patient', _username=user.username))

    flash('Invalid username or password.')
    return render_template('index.html')

@app.route('/hs/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'




#DOCTOR
""" Get doctor homepage """
@app.route('/hs/doctor/<_username>', methods=['GET','POST'])
@login_required
def doctor(_username):
    if request.method == 'GET':
        pers = Persona.query.filter_by(username=_username).first()
        doc = Medico.query.filter_by(id_medico=pers.id_persona).first()
        patients = (Paziente.query.filter_by(id_medico=doc.id_medico).all())
        return render_template('homepage/doctor.html', doctor=doc, users=patients);

""" Get info of a patient """
@app.route('/hs/info/<p_username>')
@login_required
def info(p_username):
    p = Persona.query.filter_by(username=p_username).first()
    r = Ricetta.query.filter_by(id_paziente=p.id_persona).all()
    return render_template('homepage/info.html', patient=p, prescription=r)

""" Add prescription """
@app.route('/hs/add_prescr/<id_patient>', methods=['GET', 'POST'])
@login_required
def add_prescr(id_patient):
    if request.method == 'POST':
        prescription = Ricetta()
        pat = Paziente.query.filter_by(id_paziente=id_patient).first()
        prescription.id_paziente = pat.id_paziente
        prescription.id_medico = pat.id_medico
        prescription.campo = request.form['TextPrescription']
        prescription.data_emissione = date.today()
        try:
            db.session.add(prescription)
            db.session.commit()
        except:
            db.session.rollback()
    return redirect(request.args.get('next') or url_for('info', p_username=pat.persona.username))

""" Notify the patient about a prescription ------------------------------------------------- """
@app.route('/hs/notify/<id_prescription>')
@login_required
def notify(id_prescription):
    prescr = Ricetta.query.filter_by(id_ricetta=id_prescription).first()
    p = Persona.query.filter_by(id_persona=prescr.id_paziente).first()
    email = ''
    return redirect(request.args.get('next') or url_for('info', p_username=p.username))

""" Remove prescription """
@app.route('/hs/remove_prescr/<id_prescription>')
@login_required
def remove_prescr(id_prescription):
    prescr = Ricetta.query.filter_by(id_ricetta=id_prescription).first()
    p = Persona.query.filter_by(id_persona=prescr.id_paziente).first()
    try:
        db.session.query(Ricetta).filter(Ricetta.id_ricetta==id_prescription).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(request.args.get('next') or url_for('info', p_username=p.username))

""" Add a new patient """
@app.route('/hs/newpatient', methods=['GET', 'POST'])
@login_required
def add_patient(m_username):
    if request.method == 'GET':
        return render_template('homepage/register.html')

""" Remove a patient choise """
@app.route('/hs/remove/<p_username>', methods=['GET'])
@login_required
def remove_patient(p_username):
     p = Persona.query.filter_by(username=p_username).first()
     p_info = Paziente.query.filter_by(id_paziente=p.id_persona).first()
     med = p_info.medico

     try:
         db.session.query(Ricetta).filter(Ricetta.id_paziente==p_info.id_paziente).delete()
         db.session.delete(p_info)
         db.session.delete(p)
         db.session.commit()
     except:
         db.session.rollback()

     return redirect(request.args.get('next') or url_for('doctor', _username=med.persona.username))


#PATIENT
@app.route('/hs/patient/<username>', methods=['GET','POST'])
@login_required
def patient(username):
    if request.method == 'GET':
        return render_template('homepage/patient.html', Persona=Persona);
