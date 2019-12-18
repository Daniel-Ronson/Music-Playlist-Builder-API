#update on tracks
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeValueTo":"1:00", "artist": "Led Zeppelin","title":"The Crunge"}' \
  http://127.0.0.1:5100/tracks/update
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeValueTo":"59:99", "artist": "Led Zeppelin","title":"The Song Remains The Same"}' \
  http://127.0.0.1:5100/tracks/update
  
#update playlist  
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"email": "spaghetti@AOL.com","playlistname":"MUZIK","trackartist":"Led Zeppelin","tracktitle":"Over The Hills and Far Away"}' \
  http://127.0.0.1:5000/playlist/track/add
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"email": "spaghetti@AOL.com","playlistname":"MUZIK","trackartist":"Led Zeppelin","tracktitle":"The Crunge"}' \
  http://127.0.0.1:5000/playlist/track/add


#update user
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeValueTo":"UPDATED_username","email" : "e@gmail.com"}' \
  http://127.0.0.1:5200/users/update
