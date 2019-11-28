-this is was our attempt at sharding the tracks database

WHAT WORKS: flask init will create all 3 tracks databases, and 1 main database for the other services
	   -./poptrack.sh distributes the tracks among the 3 databases

WHAT IS BROKEN: it cannot GET tracks from the databases

How to run:
export FLASK_APP=tracks.py
flask init
./poptrack.sh