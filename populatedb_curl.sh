curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"The Song Remains The Same","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"3:40","url":"http://10.0.2.15:9000/tracks/01%20The%20Song%20Remains%20The%20Same.mp3"}' \
  http://127.0.0.1:5100/tracks/insert
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"The Rain Song","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"3:40","url":"http://10.0.2.15:9000/tracks/02The%20Rain%20Song.mp3"}' \
  http://127.0.0.1:5100/tracks/insert
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Over The Hills and Far Away","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"4:00","url":"http://10.0.2.15:9000/tracks/03%20Over%20The%20Hills%20And%20Far%20Away.mp3"}' \
  http://127.0.0.1:5100/tracks/insert
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"The Crunge","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"3:40","url":"http://10.0.2.15:9000/tracks/04%20The%20Crunge.mp3"}' \
  http://127.0.0.1:5100/tracks/insert

#Users microservice ------------------
#Create User
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username":"sharkbro","firstname":"john","email":"e@gmail.com","lastname":"jones","password":"pass"}' \
  http://127.0.0.1:5200/users/create

#playlist microservice
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username":"sharkbro","firstname":"john","email":"e@gmail.com","lastname":"jones","playlistname":"tunes"}' \
  http://127.0.0.1:5000/playlist/create
  
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username":"sharkbro","firstname":"john","email":"e@gmail.com","lastname":"jones","playlistname":"BEST SONGS"}' \
  http://127.0.0.1:5000/playlist/create
  
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username":"DRon","firstname":"Danny","email":"spaghetti@AOL.com","lastname":"Bronson","playlistname":"MUZIK"}' \
  http://127.0.0.1:5000/playlist/create 

#GET from playlist

  
#Add to playlist, cant add songs that dont exist
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"email": "e@gmail.com","playlistname":"tunes","trackartist":"Led Zeppelin","tracktitle":"Over The Hills and Far Away"}' \
  http://127.0.0.1:5000/playlist/track/add
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"email": "e@gmail.com","playlistname":"tunes","trackartist":"Led Zeppelin","tracktitle":"The Crunge"}' \
  http://127.0.0.1:5000/playlist/track/add
  
  
