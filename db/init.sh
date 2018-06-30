#!/bin/sh
#   Check if you are in HealthSystem/db dir before start this script!
#   Run init files
./mongodb/init_mongodb.sh
./postgresql/init_postgresql.sh
