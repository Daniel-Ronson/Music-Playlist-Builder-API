curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"The Song Remains The Same","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"3:40","url":"http://10.0.2.15:9000/tracks/01%20The%20Song%20Remains%20The%20Same.mp3"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"The Rain Song","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"3:40","url":"http://10.0.2.15:9000/tracks/02 The%20Rain%20Song.mp3"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Over The Hills and Far Away","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"4:00","url":"http://10.0.2.15:9000/tracks/03%20Over%20The%20Hills%20And%20Far%20Away.mp3"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"The Crunge","album":"Houses Of The Holy","artist":"Led Zeppelin","duration":"3:40","url":"http://10.0.2.15:9000/tracks/04%20The%20Crunge.mp3"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username": "MickeyMouse23", "password": "tiger","firstname": "Danny","lastname": "R","email": "jdanny@gmail.com"}' \
  http://127.0.0.1:5200/api/resources/users
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"userid":"1","title":"Heavy Metal","description":"Mostly Led Zeppelin"}' \
  http://127.0.0.1:5000/playlist/create
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"trackName":"The Crunge","artist":"Led Zeppelin","playlistName":"Heavy Metal","userid":1}' \
  http://127.0.0.1:5000/playlist/track/add
