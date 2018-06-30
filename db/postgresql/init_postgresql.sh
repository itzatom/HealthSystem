#!/bin/bash

#   Create user
sudo -u postgres createuser dbahealthsystem -d -E
sudo -u postgres createdb HealthSystem -O dbahealthsystem
sudo -i -u postgres psql -c "alter USER dbahealthsystem WITH PASSWORD 'healthsystem'"


sudo -u postgres psql -d HealthSystem -U dbahealthsystem -W -f sqlfiles/postgres_ddl.sql
sudo -u postgres psql -d HealthSystem -U dbahealthsystem -W -f sqlfiles/postgres_dcl.sql 
