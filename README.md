Project Member Names:
Daniel Ronson - Ops
Jason Mora-Mendoza - Dev 1 - Sharding
Arthur Dayot - Dev 2 - XSPF

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

chmod +x poptrack.sh foreman.sh ringbalancer.sh kongconfig.sh

./kongconfig.sh
./ringbalancer.sh
flask init
./foreman.sh
./poptrack.sh

notes:
The xml is valid, open the xml in a text editor and then copy paste it into the validation: https://validator.xspf.org/
The track Urls are also valid



