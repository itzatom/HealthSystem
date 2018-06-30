#!/bin/bash

sudo -u postgres psql -d HealthSystem -U dbahealthsystem -W -f sqlfiles/postgres_ddl.sql
