#!/bin/bash

#   Create user
createuser dbahealthsystem -d -E
createdb healthsystem -O dbahealthsystem
psql -c "alter USER dbahealthsystem WITH PASSWORD 'passwddba'"

createuser medico -D -E
psql -c "alter USER medico WITH PASSWORD 'passwdmedico'"

createuser paziente -D -E
psql -c "alter USER paziente WITH PASSWORD 'passwdpaziente'"

#   Change date format from MDY (Month/Day/Year) to DMY (Day/Month/Year)
psql -c "ALTER DATABASE healthsystem SET datestyle TO 'ISO, DMY'"

psql -d healthsystem -U dbahealthsystem -W -f /scripts/ddl.sql
psql -d healthsystem -U dbahealthsystem -W -f /scripts/dcl.sql
psql -d healthsystem -U dbahealthsystem -W -f /scripts/dml.sql


#CREATE USER medico;
#ALTER USER medico WITH PASSWORD 'passwdmedico'
#CREATE USER paziente;
#alter USER paziente WITH PASSWORD 'passwdpaziente'
#GRANT CONNECT ON DATABASE healthsystem to medico;
#GRANT CONNECT ON DATABASE healthsystem to paziente;
#ALTER DATABASE healthsystem SET datestyle TO 'ISO, DMY'
#CREATE DATABASE healthsystem;
#GRANT ALL PRIVILEGES ON DATABASE healthsystem TO dbahealthsystem;
