-- :name create_track :insert
INSERT INTO tracks(title, album, artist, duration,url)
VALUES(:title, :album, :artist, :duration, :url)
