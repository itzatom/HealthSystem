DROP TABLE RICETTA CASCADE;
DROP TABLE PAZIENTE CASCADE;
DROP TABLE MEDICO CASCADE;
DROP TABLE STUD_LEG CASCADE;
DROP TABLE EMAIL CASCADE;
DROP TABLE TELEFONO CASCADE;
DROP TABLE DOCUMENTO CASCADE;
DROP TABLE PERSONA CASCADE;
DROP TABLE INDIRIZZO CASCADE;
DROP TABLE TIPO_DOC CASCADE;

CREATE TABLE TIPO_DOC
(
	ID_TIPO serial primary key,
	DOCUMENTO varchar(50)
);

CREATE TABLE INDIRIZZO
(
	ID_INDIRIZZO serial primary key,
	CAP int not null,
	INDIRIZZO varchar(100) not null
);


CREATE TABLE PERSONA
(
	ID_PERSONA serial primary key,
	NOME varchar (50) not null,
	COGNOME varchar (50) not null,
	USERNAME varchar(50) not null,
	PASSWORD varchar(50) not null,
	CF varchar (16) not null unique,
	constraint CFConsentito check(CF ~ '^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$'),
	ID_INDIRIZZO integer unique not null references INDIRIZZO(ID_INDIRIZZO),
	LUOGO_NASCITA varchar(50) not null, 
	DATA_NASCITA date not null
);

CREATE TABLE DOCUMENTO
(
	ID_DOCUMENTO varchar(50) primary key,
	ID_PERSONA integer references PERSONA(ID_PERSONA),
	ID_TIPO integer references TIPO_DOC(ID_TIPO)
);

CREATE TABLE TELEFONO
(
	NUMERO_CELLULARE varchar(11) primary key,
	ID_PERSONA integer references PERSONA(ID_PERSONA)
);


CREATE TABLE EMAIL
(
	
	EMAIL varchar(50) primary key,
	ID_PERSONA integer references PERSONA(ID_PERSONA)
);

CREATE TABLE STUD_LEG
(
	ID_STUDIO serial primary key,
	ID_INDIRIZZO integer references INDIRIZZO(ID_INDIRIZZO),
	ORARIO_INIZIO time not null,
	ORARIO_FINE time not null,
	DA_GIORNO varchar(20) not null,
	A_GIORNO varchar(20) not null

);

CREATE TABLE MEDICO
(
	ID_MEDICO integer primary key references PERSONA(ID_PERSONA),
	ID_STUDIO integer references STUD_LEG(ID_STUDIO)
);


CREATE TABLE PAZIENTE
(
	ID_PAZIENTE integer primary key references PERSONA(ID_PERSONA),
	ID_MEDICO integer references MEDICO(ID_MEDICO)
);

CREATE TABLE RICETTA
(
	ID_RICETTA serial primary key,
	ID_PAZIENTE integer references PAZIENTE(ID_PAZIENTE),
	ID_MEDICO integer references MEDICO(ID_MEDICO),
	CAMPO varchar(300) not null,
	DATA_EMISSIONE date not null
);
