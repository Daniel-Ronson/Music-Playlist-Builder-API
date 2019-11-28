-- :name update_track :insert
UPDATE tracks SET title=:title WHERE id = :id;
