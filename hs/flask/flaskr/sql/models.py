from .db_config import db
from werkzeug.security import check_password_hash, generate_password_hash


class Indirizzo(db.Model):
    __tablename__ = 'indirizzo'

    id_indirizzo = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('indirizzo_id_indirizzo_seq'::regclass)"))
    cap = db.Column(db.Integer, nullable=False)
    indirizzo = db.Column(db.String(100), nullable=False)

    def __init__(self, id_indirizzo, cap, indirizzo):
        self.id_indirizzo = id_indirizzo
        self.cap = cap
        self.indirizzo = indirizzo

    def __repr__(self):
        return '<id_indirizzo {}>'.format(self.id_indirizzo)


class TipoDoc(db.Model):
    __tablename__ = 'tipo_doc'

    id_tipo = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('tipo_doc_id_tipo_seq'::regclass)"))
    tipo_documento = db.Column(db.String(50))

    def __init(self, id_tipo, documento):
        self.id_tipo = id_tipo
        self.tipo_documento = tipo_documento

    def __repr__(self):
        return '<id_tipo {}>'.format(self.id_tipo)

class Persona(db.Model):
    __tablename__ = 'persona'
    __table_args__ = (
        db.CheckConstraint("(cf)::text ~ '^[A-Z]{6}\\d{2}[A-Z]\\d{2}[A-Z]\\d{3}[A-Z]$'::text"),
    )

    id_persona = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('persona_id_persona_seq'::regclass)"))
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    cf = db.Column(db.String(16), nullable=False, unique=True)
    id_indirizzo = db.Column(db.Integer, db.ForeignKey('indirizzo.id_indirizzo'), nullable=False, unique=True)
    luogo_nascita = db.Column(db.String(50), nullable=False)
    data_nascita = db.Column(db.Date, nullable=False)

    indirizzo = db.relationship('Indirizzo', uselist=False)

    def __init__(self, id_persona, nome, cognome, username, password, cf, id_indirizzo, luogo_nascita, data_nascita):
        self.id_persona = id_persona
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.set_password(password)
        self.cf = cf
        self.id_indirizzo = id_indirizzo
        self.luogo_nascita = luogo_nascita
        self.data_nascita = data_nascita

    def __repr__(self):
        return '<id {}>'.format(self.id_persona)

    def get_id(self):
        return self.id_persona

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class StudLeg(db.Model):
    __tablename__ = 'stud_leg'

    id_studio = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('stud_leg_id_studio_seq'::regclass)"))
    id_indirizzo = db.Column(db.Integer, db.ForeignKey('indirizzo.id_indirizzo'))
    orario_inizio = db.Column(db.Time, nullable=False)
    orario_fine = db.Column(db.Time, nullable=False)
    da_giorno = db.Column(db.String(20), nullable=False)
    a_giorno = db.Column(db.String(20), nullable=False)

    indirizzo = db.relationship('Indirizzo', foreign_keys=[id_indirizzo])

    def __init__(self, id_studio, id_indirizzo, orario_inizio, orario_fine, da_giorno, a_giorno):
        self.id_studio = id_studio;
        self.id_indirizzo = id_indirizzo
        self.orario_inizio = orario_inizio
        self.orario_fine = orario_fine
        self.da_giorno = da_giorno
        self.a_giorno = a_giorno

    def __repr__(self):
        return '<id {}>'.format(self.id_studio)


class Documento(db.Model):
    __tablename__ = 'documento'

    id_documento = db.Column(db.String(50), primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipo_doc.id_tipo'))

    persona = db.relationship('Persona')
    tipo_doc = db.relationship('TipoDoc')

    def __init__(self, id_documento, id_persona, id_tipo):
        self.id_documento = id_documento
        self.id_persona = id_persona
        self.id_tipo = id_tipo

    def __repr__(self):
        return '<id {}>'.format(self.id_documento)

class Email(db.Model):
    __tablename__ = 'email'

    email = db.Column(db.String(50), primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))

    persona = db.relationship('Persona')

    def __init__(self, email, id_persona):
        self.email = email
        self.id_persona = id_persona

    def __repr__():
        return '<email {}>'.format(self.email)

class Medico(db.Model):
    __tablename__ = 'medico'

    id_medico = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), primary_key=True)
    id_studio = db.Column(db.Integer, db.ForeignKey('stud_leg.id_studio'), unique=True)

    persona = db.relationship('Persona', foreign_keys=[id_medico])
    stud_leg = db.relationship('StudLeg', foreign_keys=[id_studio])

    def __init__(self, id_medico, id_studio):
        self.id_medico = id_medico
        self.id_studio = id_studio

    def __repr__(self):
        return '<id {}>'.format(self.id_medico)


class Telefono(db.Model):
    __tablename__ = 'telefono'

    numero_cellulare = db.Column(db.String(11), primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))

    persona = db.relationship('Persona')

    def __init__(self, numero_cellulare, id_persona):
        self.numero_cellulare = numero_cellulare
        self.id_persona = id_persona

    def __repr__(self):
        return '<phone number {}>'.format(self.numero_cellulare)

class Paziente(db.Model):
    __tablename__ = 'paziente'

    id_paziente = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), primary_key=True)
    id_medico = db.Column(db.Integer, db.ForeignKey('medico.id_medico'), nullable=False)

    def __init__(self, id_paziente, id_medico):
        self.id_paziente = id_paziente
        self.id_medico = id_medico

    def __repr__(self):
        return '<id {}>'.format(self.id_paziente)


class Ricetta(db.Model):
    __tablename__ = 'ricetta'

    id_ricetta = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('ricetta_id_ricetta_seq'::regclass)"))
    id_paziente = db.Column(db.Integer, db.ForeignKey('paziente.id_paziente'))
    id_medico = db.Column(db.Integer, db.ForeignKey('medico.id_medico'))
    campo = db.Column(db.String(300), nullable=False)
    data_emissione = db.Column(db.Date, nullable=False)

    medico = db.relationship('Medico')
    paziente = db.relationship('Paziente')

    def __init(self, id_ricetta, id_paziente, id_medico, campo, data_emissione):
        self.id_ricetta = id_ricetta
        self.id_paziente = id_paziente
        self.id_medico = id_medico
        self.campo = campo
        self.data_emissione = data_emissione

    def __repr(self):
        return '<id {}>'.format(self.id_ricetta)
