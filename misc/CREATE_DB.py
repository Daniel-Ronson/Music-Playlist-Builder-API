from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'],port=9042)
session = cluster.connect() 

def create_tables():
sql =	CREATE TABLE IF NOT EXISTS tracks (
		title text,
		album text,
		artist text,
		duration text,
		url text,
		PRIMARY KEY(album,title)
		);
