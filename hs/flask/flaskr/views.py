from flaskr import app, db, os, mongo
from flaskr import login_manager, mail
from flask import url_for, session, redirect, request, render_template, flash
from flask_login import login_user, login_required, logout_user
from flask_mail import Message
from .sql.models import Persona
from .sql.models import Medico, Paziente, Ricetta, TipoDoc, Documento, Indirizzo, Email, Telefono
from datetime import date

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/hs/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')

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

@app.route('/hs/<username>/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile(username):
    persona = Persona.query.filter_by(username=username).first()
    if request.method == 'GET':
        try:
            if persona.medico is not None:
                return render_template('homepage/edit_patient.html', user=persona)
        except:
            return render_template('homepage/edit_doctor.html', user=persona)
    pass
    """ da finire, bisogna aggiungere anche i campi in piú all'interno di edit_medico cioé quelli dello studio medico! """

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
    pat = Paziente.query.filter_by(id_paziente=id_patient).first()
    if request.method == 'GET':
        return redirect(url_for('info'), p_username=pat.persona.username)
    else:
        prescription = Ricetta()
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

""" Notify the patient about a prescription """
@app.route('/hs/notify/<id_prescription>', methods=['GET', 'POST'])
@login_required
def notify(id_prescription):
    prescr = Ricetta.query.filter_by(id_ricetta=id_prescription).first()
    p = Persona.query.filter_by(id_persona=prescr.id_paziente).first()
    try:
        msg = Message('healthsystem',recipients=[p.email.indirizzo])

        msg.body = "Hello from %s" %  prescr.medico.persona.nome + \
                    " %s " % prescr.medico.persona.cognome + \
                    "a new prescription is "  + \
                    "available in our office %s" % \
                    prescr.medico.stud_leg.indirizzo.strada + \
                    ", %s " % prescr.medico.stud_leg.indirizzo.cap + \
                    "since %s " % prescr.data_emissione + ". %s ." % prescr.campo

        mail.send(msg)
    except Exception as e:
        raise e
    return redirect(request.args.get('next') or url_for('info', p_username=p.username))

""" Remove prescription """
@app.route('/hs/remove_prescr/<id_prescription>', methods=['GET', 'POST'])
@login_required
def remove_prescr(id_prescription):
    prescr = Ricetta.query.filter_by(id_ricetta=id_prescription).first()
    p = Persona.query.filter_by(id_persona=prescr.id_paziente).first()
    try:
        db.session.delete(prescr)
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(request.args.get('next') or url_for('info', p_username=p.username))

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

     return redirect(request.args.get('next') or url_for('doctor', _username=med.persona.username))


#PATIENT
@app.route('/hs/patient/<_username>', methods=['GET','POST'])
@login_required
def patient(_username):
    if request.method == 'GET':
        return render_template('homepage/patient.html', Persona=_username);
