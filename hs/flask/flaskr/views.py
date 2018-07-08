from flaskr import app, db
from flaskr import login_manager
from flask import url_for, session, redirect, request, render_template, flash
from flask_login import login_user, login_required, logout_user
from .sql.models import Persona
from .sql.models import Medico, Paziente, Ricetta, TipoDoc, Documento, Indirizzo, Email, Telefono

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
    return render_template('homepage/info.html', patient=p)

""" Add a new patient """
@app.route('/hs/doctor/<m_username>/newpatient', methods=['GET', 'POST'])
@login_required
def add_patient(m_username):
    if request.method == 'GET':
        return render_template('homepage/register.html', m_username=m_username)

    else:
        tipo_doc = TipoDoc.query.filter_by(tipo_documento=request.form['form-type-doc'].lower()).first()
        documento = Documento(None, codice=request.form['form-document-code'].upper(), id_tipo=tipo_doc.id_tipo)
        indirizzo = Indirizzo(None, cap=request.form['form-zip-code'], strada=request.form['form-street-addr'])
        email = Email(None, indirizzo=request.form['form-email'])
        telefono = Telefono(None, numero=request.form['form-phonenumb'])

        try:
            db.session.add(documento)
            db.session.add(indirizzo)
            db.session.add(email)
            db.session.add(telefono)
            db.session.commit()
        except:
            db.session.rollback()

        p_documento = db.session.query(Documento).filter_by(codice=documento.codice).first()
        p_indirizzo = db.session.query(Indirizzo).filter_by(cap=indirizzo.cap, strada=indirizzo.strada).first()
        p_email = db.session.query(Email).filter_by(indirizzo=email.indirizzo).first()
        p_telefono = db.session.query(Telefono).filter_by(numero=telefono.numero).first()

        persona = Persona(None, nome=request.form['form-name'], cognome=request.form['form-surname'], \
                        username=request.form['form-user'], password=request.form['form-pass'],\
                        cf=request.form['form-perscode'].upper(), indirizzo=p_indirizzo, email=p_email,\
                        documento=p_documento, telefono=p_telefono, luogo_nascita=request.form['form-bplace'],\
                        data_nascita=request.form['form-bdate'])

        try:
            db.session.add(persona)
            db.session.commit()
        except:
            db.session.rollback()

        paz = Persona.query.filter_by(username=persona.username).first()
        medico = Persona.query.filter_by(username=m_username).first()

        p = Paziente(id_paziente=paz.id_persona, id_medico=medico.id_persona)

        try:
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(request.args.get('next') or url_for('doctor', _username=medico.username))


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

     return redirect(request.args.get('next') or url_for('doctor', p_username=med.persona.username))


#PATIENT
@app.route('/hs/patient/<_username>', methods=['GET','POST'])
@login_required
def patient(_username):
    if request.method == 'GET':
        return render_template('homepage/patient.html', Persona=_username);
