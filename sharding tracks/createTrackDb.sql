-- $ sqlite3 tracks.db < sqlite.sql

BEGIN TRANSACTION;
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
