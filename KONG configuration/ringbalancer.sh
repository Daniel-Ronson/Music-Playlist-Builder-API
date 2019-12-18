# create an upstream
curl -X POST http://localhost:8001/upstreams \
    --data "name=users.service"

# add two targets to the upstream
curl -X POST http://localhost:8001/upstreams/users.service/targets \
    --data "target=127.0.0.1:5201" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/users.service/targets \
    --data "target=127.0.0.1:5202" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/users.service/targets \
    --data "target=127.0.0.1:5200" \
    --data "weight=100"  
  
# create a Service targeting the Blue upstream
curl -X POST http://localhost:8001/services/ \
  --data 'name=userService' \
  --data "host=users.service" \
  --data 'paths[]=/users'

# finally, add a Route as an entry-point into the Service
curl -X POST http://localhost:8001/services/userService/routes/ \
  --data 'name=userRoute' \
  --data 'hosts[]=localhost' \
  --data 'paths[]=/users'
#-------------------------------------------------------------------------
# create an upstream
curl -X POST http://localhost:8001/upstreams \
    --data "name=playlist.service"

# add two targets to the upstream
curl -X POST http://localhost:8001/upstreams/playlist.service/targets \
    --data "target=127.0.0.1:5000" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/playlist.service/targets \
    --data "target=127.0.0.1:5001" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/playlist.service/targets \
    --data "target=127.0.0.1:5002" \
    --data "weight=100"  
  
# create a Service targeting the Blue upstream
curl -X POST http://localhost:8001/services/ \
  --data 'name=playlistService' \
  --data "host=playlist.service" \
  #--data 'paths[]=/playlist'

# finally, add a Route as an entry-point into the Service
curl -X POST http://localhost:8001/services/playlistService/routes/ \
  --data 'name=playlistRoute' \
  --data 'hosts[]=localhost' \
  --data 'paths[]=/playlist'
  #-------------------------------------------------------------------------
# create an upstream for descriptions
curl -X POST http://localhost:8001/upstreams \
    --data "name=descriptions.service"

# add two targets to the upstream
curl -X POST http://localhost:8001/upstreams/descriptions.service/targets \
    --data "target=127.0.0.1:5300" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/descriptions.service/targets \
    --data "target=127.0.0.1:5301" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/descriptions.service/targets \
    --data "target=127.0.0.1:5302" \
    --data "weight=100"  
  
# create a Service targeting the Blue upstream
curl -X POST http://localhost:8001/services/ \
  --data 'name=descriptionsService' \
  --data "host=descriptions.service" 
  #--data 'paths[]=/descriptions'

# finally, add a Route as an entry-point into the Service
curl -X POST http://localhost:8001/services/descriptionsService/routes/ \
  --data 'name=descriptionsRoute' \
  --data 'hosts[]=localhost' \
  --data 'paths[]=/descriptions'
  #-------------------------------------------------------------------------
# create an upstream for tracks
curl -X POST http://localhost:8001/upstreams \
    --data "name=tracks.service"

# add two targets to the upstream
curl -X POST http://localhost:8001/upstreams/tracks.service/targets \
    --data "target=127.0.0.1:5100" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/tracks.service/targets \
    --data "target=127.0.0.1:5101" \
    --data "weight=100"
curl -X POST http://localhost:8001/upstreams/tracks.service/targets \
    --data "target=127.0.0.1:5102" \
    --data "weight=100"  
  
# create a Service targeting the Blue upstream
curl -X POST http://localhost:8001/services/ \
  --data 'name=tracksService' \
  --data "host=tracks.service" 
  #--data 'paths[]=/descriptions'

# finally, add a Route as an entry-point into the Service
curl -X POST http://localhost:8001/services/tracksService/routes/ \
  --data 'name=tracksRoute' \
  --data 'hosts[]=localhost' \
  --data 'paths[]=/tracks'
