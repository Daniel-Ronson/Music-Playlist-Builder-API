-- $ sqlite3 big.db < sqlite.sql

BEGIN TRANSACTION;
/*
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id VARCHAR primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    duration VARCHAR,  
    url VARCHAR,     
    artUrl VARCHAR NULL,
    UNIQUE(title, artist)
);
*/
CREATE TABLE playlist (
    id INTEGER primary key,
    userid INTEGER,
    title VARCHAR,
    description VARCHAR NULL,
    UNIQUE(userid,title)
);

/*INSERT INTO playlist(userid,title,description) VALUES (1,'first playlist','cool songs');*/

DROP TABLE IF EXISTS playlist_tracks;
CREATE TABLE playlist_tracks(
    playlist_id INTEGER,
    track_id INTEGER

);


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    UNIQUE(username)
);

/*
INSERT INTO users (username,password,firstname,lastname,email) VALUES ('dan','123','danny','r','danny@gmail.com');
*/
DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description VARCHAR,
	username VARCHAR,
	url VARCHAR
);

INSERT INTO descriptions (description,username,url) VALUES ('good song','dan','c://music/uniquesong');
