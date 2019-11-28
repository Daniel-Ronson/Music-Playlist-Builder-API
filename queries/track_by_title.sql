-- :name track_by_title :one
SELECT * FROM tracks
WHERE title = :title;
