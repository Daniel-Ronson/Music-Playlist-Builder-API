
#delete from playlist  
 curl \
  --header "Content-type: application/json" \
  --request DELETE \
  --data '{"email": "e@gmail.com","playlistname":"tunes"}' \
  http://127.0.0.1:5000/playlist/delete

 curl \
  --header "Content-type: application/json" \
  --request DELETE \
  --data '{"email": "spaghetti@AOL.com","playlistname":"MUZIK"}' \
  http://127.0.0.1:5000/playlist/delete 
#delete from tracks
 curl \
  --header "Content-type: application/json" \
  --request DELETE \
  --data '{"artist": "Led Zeppelin","title":"The Song Remains The Same"}' \
  http://127.0.0.1:5100/tracks/delete 

#delete from tracks
 curl \
  --header "Content-type: application/json" \
  --request DELETE \
  --data '{"email":"email"}' \
  http://127.0.0.1:5200/users/delete 
