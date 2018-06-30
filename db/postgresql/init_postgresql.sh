#!/bin/bash
sudo -u postgres dropdb healthsystem
sudo -u postgres dropuser dbahealthsystem
sudo -u postgres dropuser paziente
sudo -u postgres dropuser medico

#   Create user
sudo -u postgres createuser dbahealthsystem -d -E
sudo -u postgres createdb healthsystem -O dbahealthsystem
sudo -i -u postgres psql -c "alter USER dbahealthsystem WITH PASSWORD 'passwddba'"

sudo -u postgres createuser medico -D -E
sudo -i -u postgres psql -c "alter USER medico WITH PASSWORD 'passwdmedico'"

sudo -u postgres createuser paziente -D -E
sudo -i -u postgres psql -c "alter USER paziente WITH PASSWORD 'passwdpaziente'"

#   Change date format from MDY (Month/Day/Year) to DMY (Day/Month/Year)
sudo -i -u postgres psql -c "ALTER DATABASE healthsystem SET datestyle TO 'ISO, DMY'"
sudo service postgresql restart 

sudo -u postgres psql -d healthsystem -U dbahealthsystem -W -f sqlfiles/postgres_ddl.sql
sudo -u postgres psql -d healthsystem -U dbahealthsystem -W -f sqlfiles/postgres_dcl.sql
sudo -u postgres psql -d healthsystem -U dbahealthsystem -W -f sqlfiles/postgres_dml.sql


#   Command for run PostgreSQL command line
sudo -u postgres psql -d healthsystem -U dbahealthsystem -W 

