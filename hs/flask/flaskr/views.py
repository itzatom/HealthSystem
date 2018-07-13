from flaskr import app, db, os, mongo, login_manager, mail
from flask import url_for, session, redirect, request, render_template, flash
from flask_login import login_user, login_required, logout_user
from flask_mail import Message
from .sql.models import Medico, Paziente, Ricetta, TipoDoc, Documento, Indirizzo, Email, Telefono, Persona, StudLeg
from datetime import date, time
import re
from bson.json_util import dumps

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
    medico = Medico.query.filter_by(id_medico=persona.id_persona).first()
    paziente = Paziente.query.filter_by(id_paziente=persona.id_persona).first()
    if request.method == 'GET':
        if medico is not None:
            return render_template('homepage/edit_doctor.html', user=medico)
        else:
            if paziente is not None:
                return render_template('homepage/edit_patient.html', user=paziente)

    if medico is not None:
        #Check if email has changed
        if medico.persona.email.indirizzo != request.form['form-email']:
            email = db.session.query(Email).filter_by(id_email=medico.persona.id_email).first()
            email.indirizzo = request.form['form-email']

        a=request.form['form-pass']
        b=request.form['conf-form-pass']
        
        #Check if password has changed
        if a is not None and b is not None:
            if a==b and len(a) > 8:
                persona.set_password(request.form['form-pass'])
            else:
                flash('Password error: less than 8 char or misplelled')
                return redirect(url_for('edit_profile', username=persona.username))

        #Check if phonenumber has changed
        if medico.persona.telefono.numero != request.form['form-phonenumb']:
            telefono = db.session.query(Telefono).filter_by(id_telefono=medico.persona.id_telefono).first()
            telefono.numero = request.form['form-phonenumb']

        #Check if  address has changed
        if medico.persona.indirizzo.strada != request.form['form-street-addr']:
            indirizzo = db.session.query(Indirizzo).filter_by(id_indirizzo=medico.persona.id_indirizzo).first()
            indirizzo.strada = request.form['form-street-addr']
            if medico.persona.indirizzo.cap != request.form['form-zip-code']:
                indirizzo.cap = request.form['form-zip-code']

        #Medical office
        #Check if address has changed
        if medico.stud_leg.indirizzo.strada != request.form['form-waddr']:
            indirizzo = db.session.query(Indirizzo).filter_by(id_indirizzo=medico.stud_leg.id_indirizzo).first()
            indirizzo.strada = request.form['form-waddr']
            if medico.stud_leg.indirizzo.cap != request.form['form-wzip-code']:
                indirizzo.cap = request.form['form-wzip-code']

        #Check if work time has changed
        #Time start
        if str(medico.stud_leg.orario_inizio.hour) is not str(request.form['form-wstart-h']):
            stud_leg = StudLeg.query.filter_by(id_studio=medico.id_studio).first()
            ora = (int(request.form['form-wstart-h']))

            if str(medico.stud_leg.orario_inizio.minute) is not str(request.form['form-wstart-m']):
                minuto = (int(request.form['form-wstart-m']))
            stud_leg.orario_inizio = time(hour=ora, minute=minuto)

        #Time end
        if str(medico.stud_leg.orario_fine.hour) is not str(request.form['form-wend-h']):
            stud_leg = StudLeg.query.filter_by(id_studio=medico.id_studio).first()
            ora = (int(request.form['form-wend-h']))

            if str(medico.stud_leg.orario_fine.minute) is not str(request.form['form-wend-m']):
                minuto = (int(request.form['form-wend-m']))
            stud_leg.orario_fine = time(hour=ora, minute=minuto)

        if stud_leg.orario_inizio >= stud_leg.orario_fine:
            flash('Start work time must be less than or equal end work time')
            return render_template('homepage/edit_doctor.html', user=medico)

        #Check if work day has changed
        if medico.stud_leg.da_giorno != str(request.form['form-fday']):
            stud_leg.da_giorno = str(request.form['form-fday'])

        #Check if work day has changed
        if medico.stud_leg.a_giorno != str(request.form['form-tday']):
            stud_leg.a_giorno = str(request.form['form-tday'])

        try:
            db.session.commit()
        except:
            db.session.rollback()

        if a is not None and b is not None:
            logout_user()
            flash('Password has changed, please log in.')
            return redirect(url_for('index'))

        return redirect(request.args.get('next') or url_for('doctor', _username=medico.persona.username))

    elif paziente is not None:

        paziente = Paziente.query.filter_by(id_paziente=persona.id_persona).first()
        mail = request.form['form-email']

        #Check if email has changed
        if paziente.persona.email.indirizzo != mail:
            email = db.session.query(Email).filter_by(id_email=paziente.persona.id_email).first()
            email.indirizzo = request.form['form-email']
        else:
            flash('Email address already used')
            return render_template('homepage/edit_patient.html', user=paziente.persona.username)

        a=request.form['form-pass']
        b=request.form['conf-form-pass']
        #Check if password has changed
        if a is not None and b is not None:
            if a==b and len(a) > 8:
                persona.set_password(request.form['form-pass'])
            else:
                flash('Password error: less than 8 char or misplelled')
                return redirect(url_for('edit_profile', username=persona.username))
        else:
            pass

        #Check if phonenumber has changed
        if medico.persona.telefono.numero != request.form['form-phonenumb']:
            telefono = db.session.query(Telefono).filter_by(id_telefono=medico.persona.id_telefono).first()
            telefono.numero = request.form['form-phonenumb']

        #Check if  address has changed
        if medico.persona.indirizzo.strada != request.form['form-street-addr']:
            indirizzo = db.session.query(Indirizzo).filter_by(id_indirizzo=medico.persona.id_indirizzo).first()
            indirizzo.strada = request.form['form-street-addr']
            if medico.persona.indirizzo.cap != request.form['form-zip-code']:
                indirizzo.cap = request.form['form-zip-code']

        try:
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(request.args.get('next') or url_for('patient', _username=paziente.persona.username))

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
    hspurp = mongo.db.biometrics
    datelist = hspurp.find( { "username": p.username}, {"_id": 0, "date": 1 })
    return render_template('homepage/info.html', patient=p, prescription=r, hpdate=datelist)

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

        indirizzo = Indirizzo(None, cap=request.form['form-zip-code'], strada=request.form['form-street-addr'])

        tipo_doc = TipoDoc.query.filter_by(tipo_documento=request.form['form-type-doc'].lower()).first()
        doc = db.session.query(Documento).filter_by(codice=request.form['form-document-code'].upper()).first()
        if doc is None:
            documento = Documento(None, codice=request.form['form-document-code'].upper(), id_tipo=tipo_doc.id_tipo)
        else:
            flash('document is already used')
            return render_template('homepage/register.html', m_username=m_username)

        mail = db.session.query(Email).filter_by(indirizzo=request.form['form-email']).first()
        if  mail is None:
            email = Email(None, indirizzo=request.form['form-email'])
        else:
            flash('Email address already used')
            return render_template('homepage/register.html', m_username=m_username)

        tel = db.session.query(Telefono).filter_by(numero=request.form['form-phonenumb']).first()
        if tel is None:
            telefono = Telefono(None, numero=request.form['form-phonenumb'])
        else:
            flash('Phone number already used')
            return render_template('homepage/register.html', m_username=m_username)

        #regexp
        if db.session.query(Persona).filter_by(cf=request.form['form-perscode'].upper()).first() is None:
            p_cf = request.form['form-perscode'].upper()
            if p_cf is not None:
                if re.match('^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$',p_cf) is None:
                    flash('CF is not valid, please insert a valid one')
                    return render_template('homepage/register.html', m_username=m_username)
        else:
            flash('CF is already used')
            return render_template('homepage/register.html', m_username=m_username)


        p_documento = db.session.query(Documento).filter_by(codice=documento.codice).first()
        p_indirizzo = db.session.query(Indirizzo).filter_by(cap=indirizzo.cap, strada=indirizzo.strada).first()
        p_email = db.session.query(Email).filter_by(indirizzo=email.indirizzo).first()
        p_telefono = db.session.query(Telefono).filter_by(numero=telefono.numero).first()

        persona = Persona()
        persona.nome = request.form['form-name']
        persona.cognome = request.form['form-surname']
        persona.username = request.form['form-user']
        persona.password = request.form['form-pass']
        persona.cf = p_cf
        persona.indirizzo = indirizzo
        persona.email = email
        persona.documento = documento
        persona.telefono = telefono
        persona.luogo_nascita = request.form['form-bplace']
        persona.data_nascita = request.form['form-bdate']


        try:
            db.session.add(documento)
            db.session.add(indirizzo)
            db.session.add(email)
            db.session.add(telefono)
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

""" Remove a patient """
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


@app.route('/hs/request_info/<username>',methods=['POST'])
@login_required
def request_info(username):
    if request.method == 'POST':
        selected = request.form.get('data')
        page = request.form.get('dataselected')

        if page == 'biometrics':
            collection = mongo.db.biometrics
            data = collection.find({"username":username, "date":selected},{"_id":0})
            return render_template('homepage/biometrics.html', data=data[0])

        elif page == 'health_data':
            collection = mongo.db.health_purpose
            data = collection.find({"username":username, "date":selected},{"_id":0})
            return render_template('homepage/healthdata.html', data=data[0])

@app.route('/hs/about',methods=['GET','POST'])
def about():
    return render_template('homepage/about.html')

#PATIENT
@app.route('/hs/patient/<_username>', methods=['GET','POST'])
@login_required
def patient(_username):
    if request.method == 'GET':
        persona = Persona.query.filter_by(username=_username).first()
        paziente = Paziente.query.filter_by(id_paziente=persona.id_persona).first()
        return render_template('homepage/patient.html', paziente=paziente);
