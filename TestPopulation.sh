curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Test Insert song 1","album":"Test Album 1","artist":"Test artist 1","duration":"3:40","url":"C://songs/s23","arturl":"C;//song/img/s23"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Test Insert Song 2","album":"Test Album 2","artist":"Test artist 2","duration":"4:10","url":"C://songs/s23","arturl":"C;//song/img/s23"}' \
  http://127.0.0.1:5100/api/resources/tracks
	curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Danger Zone","album":"Top Gun","artist":"Kenny Loggins","duration":"3:32","url":"https://www.youtube.com/watch?v=yK0P1Bk8Cx4","arturl":"https://upload.wikimedia.org/wikipedia/en/2/2c/Loggins_-_Danger_Zone_single_cover.png"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"title":"Never Gonna Give You Up","album":"Whenever You Need Somebody","artist":"Rick Astley","duration":"3:33","url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","arturl":"https://upload.wikimedia.org/wikipedia/en/3/34/RickAstleyNeverGonnaGiveYouUp7InchSingleCover.jpg"}' \
  http://127.0.0.1:5100/api/resources/tracks
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username": "ArthurDayot123", "password": "elephant","firstname": "Arthur","lastname": "Dayot","email": "adayot0@csu.fullerton.edu"}' \
  http://127.0.0.1:5200/api/resources/users
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"username": "JoeSchmoe", "password": "tiger","firstname": "Joe","lastname": "Schmoe","email": "joe@schmoe.com"}' \
  http://127.0.0.1:5200/api/resources/users
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"description":"Test update description Up","username":"ArthurDayot123","url":"C;//song/img/s23"}' \
  http://127.0.0.1:5300/api/resources/descriptions
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"userid":2,"title":"Random Songs","description":"This playlist contains random songs"}' \
  http://127.0.0.1:5000/playlist/create
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"trackName":"Danger Zone","artist":"Kenny Loggins","playlistName":"Random Songs","userid":2}' \
  http://127.0.0.1:5000/playlist/track/add
curl \
  --header "Content-type: application/json" \
  --request POST \
  --data '{"trackName":"Never Gonna Give You Up","artist":"Rick Astley","playlistName":"Random Songs","userid":2}' \
  http://127.0.0.1:5000/playlist/track/add

