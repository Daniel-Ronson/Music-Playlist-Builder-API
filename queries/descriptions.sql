-- :name get_descriptions :many
SELECT username, url, description FROM descriptions WHERE username = :username AND url = :url;
