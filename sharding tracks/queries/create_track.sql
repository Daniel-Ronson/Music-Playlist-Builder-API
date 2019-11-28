-- :name create_track :insert
INSERT INTO tracks(id, title, album, artist, duration,url)
VALUES(:id, :title, :album, :artist, :duration, :url)
