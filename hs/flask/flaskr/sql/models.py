# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Table, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash



Base = declarative_base()
metadata = Base.metadata


class Indirizzo(Base):
    __tablename__ = 'indirizzo'

    id_indirizzo = Column(Integer, primary_key=True, server_default=text("nextval('indirizzo_id_indirizzo_seq'::regclass)"))
    cap = Column(Integer, nullable=False)
    indirizzo = Column(String(100), nullable=False)


class TipoDoc(Base):
    __tablename__ = 'tipo_doc'

    id_tipo = Column(Integer, primary_key=True, server_default=text("nextval('tipo_doc_id_tipo_seq'::regclass)"))
    documento = Column(String(50))


class Persona(Base):
    __tablename__ = 'persona'
    __table_args__ = (
        CheckConstraint("(cf)::text ~ '^[A-Z]{6}\\d{2}[A-Z]\\d{2}[A-Z]\\d{3}[A-Z]$'::text"),
    )

    id_persona = Column(Integer, primary_key=True, server_default=text("nextval('persona_id_persona_seq'::regclass)"))
    nome = Column(String(50), nullable=False)
    cognome = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    cf = Column(String(16), nullable=False, unique=True)
    id_indirizzo = Column(ForeignKey('indirizzo.id_indirizzo'), nullable=False, unique=True)
    luogo_nascita = Column(String(50), nullable=False)
    data_nascita = Column(Date, nullable=False)

    indirizzo = relationship('Indirizzo', uselist=False)
    stud_leg = relationship('StudLeg', secondary='medico')

<<<<<<< HEAD
    def set_password(self, password):
         self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

=======
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
>>>>>>> 2b4bc278b9007272e00124e90a2a6842747c8fc2

class StudLeg(Base):
    __tablename__ = 'stud_leg'

    id_studio = Column(Integer, primary_key=True, server_default=text("nextval('stud_leg_id_studio_seq'::regclass)"))
    id_indirizzo = Column(ForeignKey('indirizzo.id_indirizzo'))
    orario_inizio = Column(Time, nullable=False)
    orario_fine = Column(Time, nullable=False)
    da_giorno = Column(String(20), nullable=False)
    a_giorno = Column(String(20), nullable=False)

    indirizzo = relationship('Indirizzo')


class Documento(Base):
    __tablename__ = 'documento'

    id_documento = Column(String(50), primary_key=True)
    id_persona = Column(ForeignKey('persona.id_persona'))
    id_tipo = Column(ForeignKey('tipo_doc.id_tipo'))

    persona = relationship('Persona')
    tipo_doc = relationship('TipoDoc')


class Email(Base):
    __tablename__ = 'email'

    email = Column(String(50), primary_key=True)
    id_persona = Column(ForeignKey('persona.id_persona'))

    persona = relationship('Persona')

class Medico(Base):
    __tablename__ = 'medico'

    id_medico = Column(ForeignKey('persona.id_persona'), primary_key=True)
    id_studio = Column(ForeignKey('stud_leg.id_studio'))

class Telefono(Base):
    __tablename__ = 'telefono'

    numero_cellulare = Column(String(11), primary_key=True)
    id_persona = Column(ForeignKey('persona.id_persona'))

    persona = relationship('Persona')


class Paziente(Base):
    __tablename__ = 'paziente'

    id_paziente = Column(ForeignKey('persona.id_persona'), primary_key=True)
    id_medico = Column(ForeignKey('medico.id_medico'))

class Ricetta(Base):
    __tablename__ = 'ricetta'

    id_ricetta = Column(Integer, primary_key=True, server_default=text("nextval('ricetta_id_ricetta_seq'::regclass)"))
    id_paziente = Column(ForeignKey('paziente.id_paziente'))
    id_medico = Column(ForeignKey('medico.id_medico'))
    campo = Column(String(300), nullable=False)
    data_emissione = Column(Date, nullable=False)

    medico = relationship('Medico')
    paziente = relationship('Paziente')
