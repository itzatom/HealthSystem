#   Installing Mongo DB on Ubuntu 16.04

#   From www.digitalocean.com
#   MongoDB is already included in Ubuntu package repositories,
#   but the official MongoDB repository provides most up-to-date version and is the recommended way of installing the software.
#   In this step, we will add this official repository to our server.
#   Ubuntu ensures the authenticity of software packages by verifying that they are signed with GPG keys,
#   so we first have to import they key for the official MongoDB repository.
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get update

#   Now we can install the MongoDB package itself.
sudo apt-get install -y mongodb-org

#   Next, start MongoDB with systemctl.
sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod

#   Installing PostegreSQL on Ubuntu 16.04

#   From www.digitalocean.com
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

#   Restart PostegreSQL
sudo /etc/init.d/postgresql status
sudo service postgresql start
sudo service postgresql restart

#   Create user
sudo -i -u postgres psql -c "CREATE USER dbahealthsystem WITH PASSWORD 'healthsystem';"
sudo -u postgres createdb -O dbahealthsystem HealthSystem

sudo /etc/init.d/postgresql reload



