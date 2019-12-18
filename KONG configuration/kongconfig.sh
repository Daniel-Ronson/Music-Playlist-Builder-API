curl -i -X POST \
  --url http://localhost:8001/services/ \
  --data 'name=media' \
  --data 'url=http://10.0.2.15:9000'
curl -i -X POST \
  --url http://localhost:8001/services/media/routes \
  --data 'name=mediaRoute' \
  --data 'hosts[]=localhost'\
  --data 'paths[]=/media' 

