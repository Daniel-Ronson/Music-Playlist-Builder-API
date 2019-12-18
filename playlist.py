import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import requests
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
from cassandra.cluster import Cluster
from cassandra import ReadTimeout
import json
cluster = Cluster(['172.17.0.2'],port=9042)
session = cluster.connect() 
session.execute('USE Music')

# {"username":"sharkbro","firstname":"john","email":"e@gmail.com","lastname":"jones","playlistname":"tunes"}
@app.route('/playlist/create', methods=['GET','POST'])
def insert_playlist_service():
    if request.method == 'GET':
        return get_all_playlists() 
    elif request.method == 'POST':
        return insert_playlist(request.data)
       
def insert_playlist(playlist):
    username = playlist['username']
    firstname = playlist['firstname']
    lastname = playlist['lastname']
    email = playlist['email']
    playlistname = playlist['playlistname']
    #tracklist = playlist['tracklist']
    
    sql = "INSERT INTO playlist (username,firstname,lastname,email,playlistname) VALUES (%s,%s,%s,%s,%s)"
    try:
        session.execute(sql,(username,firstname,lastname,email,playlistname))
        return playlist, status.HTTP_201_CREATED
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
@app.route('/playlist/all', methods=['GET'])
def get_all_playlists_service():
    return get_all_playlists()
         
def get_all_playlists():
    row_array = []
    rows = session.execute('SELECT * from playlist')
    for item in rows:
        song =  {"username":item.username,"email":item.email, "playlistname": item.playlistname, "tracklist":str(item.tracklist) }
        row_array.append(song)
    return list(row_array)
 
 
#select playlist based on playlist name and user
#http://127.0.0.1:5000/playlist/select/user?email=e@gmail.com&playlistname=tunes
@app.route('/playlist/select',methods=['GET'])
def select_playlist_service():
    if request.method == 'GET':
        return filter_select_playlist(request.args)
     
#Search for track based off email and playlistname
def filter_select_playlist(query_parameters):
    
    email = query_parameters.get('email')
    playlistname = query_parameters.get('playlistname')
    query = "SELECT * FROM playlist WHERE email= %s AND playlistname =%s ALLOW FILTERING"
    res = session.execute_async(query, (email,playlistname))
    row_array = []
    
    try:
        rows = res.result()
        item = rows[0]
        song =  {"username":item.username,"email":item.email,"playlistname": item.playlistname,"tracklist":str(item.tracklist)}
        row_array.append(song)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return dict(row_array)


#select all playlist from a specific user
#http://127.0.0.1:5000/playlist/select/user?email=e@gmail.com
@app.route('/playlist/select/user',methods=['GET'])
def select_playlist_user_service():
    if request.method == 'GET':
        return filter_select_user_playlist(request.args)
     
#Search for track based off email and playlistname
def filter_select_user_playlist(query_parameters):
    
    email = query_parameters.get('email')
    query = "SELECT * FROM playlist WHERE email= %s ALLOW FILTERING"
    res = session.execute(query, (email,))
    row_array = []
    
    try:
        for item in res:
            playlist =  {"username":item.username,"email":item.email,"playlistname": item.playlistname,"tracklist":str(item.tracklist)}
            row_array.append(playlist)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return list(row_array)






#delete playlist based off email and playlistname
@app.route('/playlist/delete',methods=['GET','DELETE'])
def delete_playlist_service():
    if request.method == 'GET':
        return get_all_playlists()
    if request.method == 'DELETE':
        return filter_delete_playlist(request.data)
     
def filter_delete_playlist(data):
    email = data['email']
    playlistname = data['playlistname']
    query = "DELETE FROM playlist WHERE email= %s AND playlistname =%s"
    
    session.execute_async(query, (email,playlistname))         
    return '', status.HTTP_204_NO_CONTENT
 
 
 

    
#GET: give email and playlistname
#Post: give email, playlistname, trackartist, tracktitle
# {"email": "hey","playlistname":"hi","trackartist":"The Beatles","tracktitle":"Yellow Submarine"}
@app.route('/playlist/track/add', methods=['GET','PUT'])
def add_track_to_playlist():
    if request.method == 'GET':
        return filter_select_playlist(request.args)
    if request.method =='PUT':
        return playlist_add_track(request.data)

def playlist_add_track(playlist_info):
    playlist = playlist_info
    if 'email' in playlist and 'playlistname' in playlist and 'trackartist' in playlist and 'tracktitle' in playlist:
        trackName = playlist['tracktitle']
        artist = playlist['trackartist']
        playlistName = playlist['playlistname']
        email = playlist['email']
        trackData = filter_select_track_for_playlist(trackName,artist)
        track_uuid = str(trackData[0]['uuid'])
        query_insert_track = "UPDATE playlist SET tracklist = tracklist + {%s} WHERE playlistname=%s AND email=%s"
        session.execute_async(query_insert_track,(track_uuid,playlistName,email))
        return playlist, status.HTTP_201_CREATED 
     
#input artist and title for track info
@app.route('/playlist/get/track/info',methods=['GET'])
def select_track_for_playlist__service():
    if request.method == 'GET':
        return filter_select_track_for_playlist(request.args)
     
#Search for track based off given parameter
def filter_select_track_for_playlist(trackName,trackArtist):
    
    title = trackName
    artist = trackArtist
    query = "SELECT * FROM tracks WHERE title= %s AND artist= %s ALLOW FILTERING;"
    res = session.execute_async(query, (title,artist))
    row_array = []
    
    try:
        rows = res.result()
        item = rows[0]
        song =  {"uuid":item.id,"title":item.title, "album":item.album}
        row_array.append(song)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return list(row_array)    

 
#select playlist based on playlist name and user
#http://127.0.0.1:5000/playlist/select/user?email=e@gmail.com&playlistname=tunes
@app.route('/playlist/select/tracks',methods=['GET'])
def select_playlist_tracks_service():
    if request.method == 'GET':
        return filter_select_playlist_tracks(request.args)
     
#Search for track based off email and playlistname
def filter_select_playlist_tracks(query_parameters):
    
    email = query_parameters.get('email')
    playlistname = query_parameters.get('playlistname')
    query = "SELECT * FROM playlist WHERE email= %s AND playlistname =%s ALLOW FILTERING"
    res = session.execute_async(query, (email,playlistname))
    row_array = []
    track_list = []
    
    try:
        rows = res.result()
        item = rows[0]
        playlist =  {"username":item.username,"email":item.email,"playlistname": item.playlistname,"tracklist":item.tracklist}
        for track in item.tracklist:
            track_list.append(track)
        track_dict = {'tracks' : track_list}
        row_array.append(playlist)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return list(track_list)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>SPOTIFY, but without music streaming</h1>
<p>Playlist Microservice</p>'''
