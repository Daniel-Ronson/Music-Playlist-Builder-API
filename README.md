Daniel Ronson - Dev

##############
# How to run #
##############

Prerequisites:
Running on a Linux OS.
Python installed.
Flask installed.
Kong Installed, running, and configured
Minio Installed, running, and populated with tracks

Commands (in order) to run to start:
export FLASK_APP=tracks.py

chmod +x populatedb_curl.sh foreman.sh ringbalancer.sh kongconfig.sh

./kongconfig.sh
./ringbalancer.sh

flask init
./foreman.sh
./populatedb_curl.sh


View Project Documentation for endpoint descriptions



