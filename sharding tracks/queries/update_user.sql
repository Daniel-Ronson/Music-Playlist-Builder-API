-- :name update_user :insert
UPDATE users SET title=:title WHERE id = :id;
