-- $ sqlite3 music.db < sqlite.sql

BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR,
    album VARCHAR,
    artist VARCHAR,
    duration VARCHAR,  
    url VARCHAR,     
    UNIQUE(title, artist)
);


DROP TABLE IF EXISTS playlist;
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
    track_id INTEGER,

    FOREIGN KEY (playlist_id) REFERENCES playlist(id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE

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
	url VARCHAR,
	FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (url) REFERENCES tracks(url) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO descriptions (description,username,url) VALUES ('good song','dan','c://music/uniquesong');
