import sys
import json
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import uuid
app = flask_api.FlaskAPI(__name__)
from cassandra import ReadTimeout
app.config.from_envvar('APP_CONFIG')


from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'],port=9042)
session = cluster.connect() 
session.execute('USE Music')

@app.cli.command('init')
def init_db():
    return  '<h1> To init db run CREATe_DB.py </h1>'

@app.route('/conn', methods=['GET'])
def test_conn():
    return get_all_tracks()
    
@app.route('/tracks/insert', methods=['GET','POST'])
def insert_route():
    if request.method == 'GET':
        return get_all_tracks() 
    elif request.method == 'POST':
        return insert_track(request.data)

  
    
#{"album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","title":"Yellow Submarine","url":"C://songs/s23"}
#todo: add map to link descriptions to users, in users.py
def insert_track(track):
    trackid = uuid.uuid4()
    title = track['title']
    album = track['album']
    artist = track['artist']
    duration = track['duration']
    url = track['url']

    sql = "INSERT INTO tracks (id,album,artist,duration,title,url) VALUES (%s,%s,%s,%s,%s,%s)"   
    try:
        session.execute(sql,(trackid,album,artist,duration,title,url))
        return title, status.HTTP_201_CREATED
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
def get_all_tracks():
    row_array = []
    rows = session.execute('SELECT * from tracks')
    for track in rows:
        #song  = {"test":"test"}
        song =  {"uuid":track.id,"title":track.title, "artist":track.artist,"album": track.album,"duration": track.duration, "url":track.url }
        row_array.append(song)

    return list(row_array)
    
#GET track that matches id number
@app.route('/get/track/<uuid:id>', methods=['GET'])
def get_track_by_id_service(id):
    return get_track_by_id(id);
    
def get_track_by_id(id):
    
    uuid = id
    #query = "SELECT * FROM tracks WHERE title = 'newsong' AND artist= %s ALLOW FILTERING;"
    query = "SELECT * FROM tracks WHERE id= %s ALLOW FILTERING;"
    res = session.execute_async(query, [uuid])
    row_array = []
    try:
        rows = res.result()
        track = rows[0]
        song =  {"uuid":track.id,"title":track.title, "artist":track.artist,"album": track.album,"duration": track.duration, "url":track.url }
        row_array.append(song)
        
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
        
    return list(row_array)

#takes id as query string 
@app.route('/get/track/id', methods=['GET'])
def get_track_by_id_service_2():
    return get_track_by_id_2(request.args);
    
def get_track_by_id_2(data):
    
    track_uuid = data.get('id')
    track_uuid_conversion = uuid.UUID(track_uuid)
    #query = "SELECT * FROM tracks WHERE title = 'newsong' AND artist= %s ALLOW FILTERING;"
    query = "SELECT * FROM tracks WHERE id= %s ALLOW FILTERING;"
    res = session.execute_async(query, [track_uuid_conversion])
    row_array = []
    try:
        rows = res.result()
        track = rows[0]
        song =  {"uuid":str(track.id),"title":track.title, "artist":track.artist,"album": track.album,"duration": track.duration, "url":track.url }
        row_array.append(song)
        
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
        
    return list(row_array)



        
#GET track that matches url
@app.route('/get/track/url/<string:url>', methods=['GET'])
def get_track_by_url_service(url):
    return get_track_by_url(url);
    
def get_track_by_url(url):
    
    track_url = url
    #query = "SELECT * FROM tracks WHERE title = 'newsong' AND artist= %s ALLOW FILTERING;"
    query = "SELECT * FROM tracks WHERE url= %s ALLOW FILTERING;"
    res = session.execute_async(query, [track_url])
    row_array = []
    try:
        rows = res.result()
        track = rows[0]
        song =  {"uuid":track.id,"title":track.title, "artist":track.artist,"album": track.album,"duration": track.duration, "url":track.url }
        row_array.append(song)
        
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
        
    return list(row_array)    
    
     
@app.route('/tracks/update', methods=['GET','PUT'])
def updates():
    if request.method == 'GET':
        return get_all_tracks()
    if request.method == 'PUT':
        return update_track(request.data) 
        
#this method updates the duration, Cassandra can't update prmary keys
#{"changeValueTo":"Yellow Submarine", "artist": "The Beatles","title":"old song"}
def update_track(track):
    try: 
        title = track['title']
        artist = track['artist']
        changeValueTo = track['changeValueTo']    
        query_update_track = "UPDATE tracks SET duration = %s WHERE artist=%s AND title=%s"
        session.execute_async(query_update_track,(changeValueTo,artist,title))
        
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_304_NOT_MODIFIED
    return track, status.HTTP_201_CREATED


        
@app.route('/tracks/delete', methods=['GET','DELETE'])
def deletes():
    if request.method =='GET':
        return get_all_tracks()
    if request.method == 'DELETE':
        return delete_track(request.data)
        
def delete_track(track):
    title = track['title']
    artist = track['artist']
    try:
        query = "DELETE FROM tracks WHERE artist=%s AND title=%s"
        session.execute_async(query,(artist,title))
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
    return '', status.HTTP_204_NO_CONTENT






@app.route('/', methods=['GET'])
def home():
    return '''<h1>SPOTIFY, but without music streaming</h1>
    <h2>TRACKS MICROSERVICE</h2>
<p>A prototype API for delivering track, playlist, and user data.</p>'''



    

