#   Check if you are in HealthSystem dir before start this script!

#   Install python3
sudo apt-get install python3

#   Install pip3
sudo apt-get install python3-pip
pip3 install --upgrade pip

#   Setup virtual environment
sudo apt-get install python3-virtualenv
virtualenv venv

#   Run virtual environment
source venv/bin/activate

#   Install library and framework in virtual environment
pip3 install --user -r requirements.txt
