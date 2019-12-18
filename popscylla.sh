curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Test Insert song 1","album":"Test Album 1","artist":"Test artist 1","duration":"3:40","url":"C://songs/s23"}' \
  http://127.0.0.1:5000/insert

title = 'title'
album = 'album'
artist = 'artist'
duration = 'dur'
url = 'url'
