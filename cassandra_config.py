import sys
from cassandra.cluster import Cluster
from cassandra import ReadTimeout


cluster = Cluster(['172.17.0.2'],port=9042)
session = cluster.connect()


cmd = "CREATE KEYSPACE Music WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}"
session.execute(cmd)

cmd = "USE Music"

session.execute(cmd)

cmd = ("""CREATE TABLE IF NOT EXISTS tracks (
	id uuid,
	title text,
	album text,
	artist text,
	duration text,
	url text,
	PRIMARY KEY(title,artist)
	)
	""")
session.execute(cmd)

cmd = ("""
CREATE TABLE IF NOT EXISTS playlist (
	username text,
	firstname text,
	lastname text,
	email text,
	playlistname text,
	tracklist set<text>,
	PRIMARY KEY(playlistname,email)
)
""")	
session.execute(cmd)

cmd = ("""
CREATE TABLE IF NOT EXISTS users (
	username text,
	password text,
	firstname text,
	lastname text,
	email text,
	description map <uuid,text>,
	PRIMARY KEY(email)	
)
""")
session.execute(cmd)
