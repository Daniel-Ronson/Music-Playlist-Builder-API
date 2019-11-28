import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('createdb.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>SPOTIFY, but without music streaming</h1>
<p>Playlist Microservice</p>'''

#GET all playlist that matches user id number
@app.route('/playlist/select/<int:id>', methods=['GET'])
def playlist_selection(id):
    to_filter = []
    to_filter.append(id)
    query = "SELECT * FROM playlist WHERE id=?"
    results = queries._engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))
   
#list all the playlists
@app.route('/playlist/all', methods=['GET'])
def select_all():
    all_playlists = queries.select_all_playlist()
    if all_playlists:
        return list(all_playlists)
    return '<h1>No Playlist in database</h1>'

#POST - create a playlist
#GET - enter id of playlist to display it
#POST dict - {"userid":"2","title":"Hip hop","description":"only hip hop"}
@app.route('/playlist/create', methods=['GET', 'POST'])
def playlist_creation():
    if request.method == 'GET':
        return filter_playlist(request.args)
    elif request.method == 'POST':
        return create_playlist(request.data)
        
def create_playlist(playlist):
    playlist = request.data
   # required_fields = ['userid', 'title', 'descrtiption']

    #if not all([field in playlist for field in required_fields]):
     #   raise exceptions.ParseError()
    query = "INSERT INTO playlist (title,userid,description) VALUES (?,?,?)"
    to_filter = []
    to_filter.append(playlist['title'])
    to_filter.append(playlist['userid'])
    to_filter.append(playlist['description'])
    queries._engine.execute(query,to_filter)
   # try:
    #    playlist['id'] = queries.create_playlist(**playlist)
    #except Exception as e:
     #   return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return playlist, status.HTTP_201_CREATED  
    
#Populate a playlist
#POST - required fields: track name, track artist; playlist name, userid    
#{"trackName":"song title","artist":"artist name","playlistName":"first playlist","userid":"1"}
#{"trackName":"Yellow Submarine","artist":"The Beatles","playlistName":"first playlist","userid":"1"}
@app.route('/playlist/track/add', methods=['GET','POST'])
def add_track_to_playlist():
    if request.method == 'GET':
        return filter_playlist_tracks(request.args)
    if request.method =='POST':
        return playlist_add_track(request.data)

def playlist_add_track(playlist_info):
    playlist = playlist_info
    if 'trackName' in playlist and 'artist' in playlist and 'playlistName' in playlist and 'userid' in playlist:
        trackName = playlist['trackName']
        artist = playlist['artist']
        playlistName = playlist['playlistName']
        userid = playlist['userid']
        select_track_query = "SELECT id FROM tracks WHERE title=? AND artist=?"
        to_filter_track =[]
        to_filter_track.append(trackName)
        to_filter_track.append(artist)
        #track_info = queries._engine.execute(select_track_query,to_filter_track).fetchone()
        
      #  for row in track_info:
       #     track_id= row[0]
       
        select_playlist_query = "SELECT id FROM playlist WHERE title=? AND userid=?"
        to_filter_track.append(playlistName)
        to_filter_track.append(userid)
       # playlist_info = queries._engine.execute(select_track_query,to_filter_playlist).fetchone()
        
        #for row in playlist_info:
         #   playlistid = row[0]
         
        query_insert_track = ("INSERT INTO playlist_tracks (track_id,playlist_id) VALUES "
                            "((SELECT id FROM tracks WHERE title=? AND artist=?),"
                            "(SELECT id FROM playlist WHERE title=? AND userid=?))")

        queries._engine.execute(query_insert_track,to_filter_track)
        return playlist, status.HTTP_201_CREATED 
    

def filter_playlist_tracks(query_parameters):
    id = query_parameters.get('playlistid')    
    query = "SELECT * FROM playlist_tracks WHERE"
    to_filter = []
    if id:
        query += ' playlist_id=?'
        to_filter.append(id)
    if not (id):
        raise exceptions.NotFound()
    results = queries._engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))
    
#Retrieve a playlist
#required field - playlist id
@app.route('/playlist/display', methods=['GET', 'POST'])
def playlist_select_one():
    if request.method == 'GET':
        return filter_playlist(request.args)
        
def filter_playlist(query_parameters):
    id = query_parameters.get('id')
    query = "SELECT * FROM playlist WHERE"
    to_filter = []

    if id:
        query += ' id=?'
        to_filter.append(id)

    if not (id):
        raise exceptions.NotFound()

    query_two = "SELECT * FROM playlist_tracks WHERE playlist_id=?"
    results_playlist = queries._engine.execute(query, to_filter).fetchall()
    results_tracks = queries._engine.execute(query_two, to_filter).fetchall()
    full_playlist = {
    "playlist description":results_playlist,
    "playlist tracks":results_tracks
    }
    return list(map(dict, results_playlist)) and list(map(dict, results_tracks))
    
@app.route('/playlist/delete/<int:id>', methods=['GET','DELETE'])
def deletes(id):
    if request.method =='GET':
        all_playlists = queries.select_all_playlist()
        if all_playlists:
            return list(all_playlists)
    if request.method == 'DELETE':
        return delete_playlist(id)
        
def delete_playlist(id):
    playlistid = id
    filter_query =[]
   # query = "DELETE FROM playlist WHERE id=?"
    query = "DELETE FROM playlist WHERE userid = ?"
    filter_query.append(playlistid)
    queries._engine.execute(query,filter_query)
   # except Exception as e:
    #    return { 'error': str(e) }, status.HTTP_404_NOT_FOUND
    return '', status.HTTP_204_NO_CONTENT
