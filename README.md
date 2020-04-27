Author: Daniel Ronson

## Overview
- REST microservices
- Create and manage playlists
- Generate XSPF format playlist
- Servies: XMLGEN, playlists, tracks, descriptions, users
- Flask web framework

## Prerequisites:
- Running on a Linux OS
- Python3 installed.
- Flask installed.
- Kong Installed, running, and configured
- Minio Installed, running, and populated with tracks
- install python requets
- install cassandra driver for python

## How to run one services
1. export FLASK_APP=tracks.py
2. chmod +x populatedb_curl.sh foreman.sh ringbalancer.sh kongconfig.sh
3. `./kongconfig.sh` ` Initializes Kong
3. `./ringbalancer.sh` Configures load balancer
4. `python  cassandra_config.py` creates database schema
5 `./foreman.sh` Spawns desired amount of each service, I configured 3 of each in Kong
6. `./populatedb_curl.sh` Populates database with content

## Now you can 
- Consume any endpoint describbed in API documentation through load balancer or by exact address
- Generate XSPF playlists by using the XMLGEN.py microservice
- Note: Music files must be stored in minio to actually listen to the playlist

## Load balancer 
 - access load balancer at localhost:8000/<serviceName>/<serviceEndpoint
 - example query: `localhost:8000/playlist/playlist/all`






