-- :name create_user :insert
INSERT INTO users(username, password, firstname, lastname, email)
VALUES(:username, :password, :firstname, :lastname, :email)
