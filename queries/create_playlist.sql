-- :name create_playlist :insert
INSERT INTO playlist(userid, title, description)
VALUES(:userid, :title, :description)
