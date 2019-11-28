#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import json
import pugsql
import uuid
import sqlite3
sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b)) #convert sqlire types to python types
sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le)) #convert python types to sqlite types
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
queries = pugsql.module('queries/')
queries1 = pugsql.module('queries/')
queries2 = pugsql.module('queries/')
queries3 = pugsql.module('queries/')

queries.connect(app.config['DATABASE_URL'])
queries1.connect(app.config['TRACKS_ONE'])
queries2.connect(app.config['TRACKS_TWO'])
queries3.connect(app.config['TRACKS_THREE'])
 
@app.cli.command('init')
def init_db():
    create_db('DATABASE_URL','createdb.sql')
    create_db('TRACKS_ONE','createTrackDb.sql')
    create_db('TRACKS_TWO','createTrackDb.sql')
    create_db('TRACKS_THREE','createTrackDb.sql')

def create_db(DATABASE_URL,CreateDb):
    with app.app_context():
        queries.connect(app.config[DATABASE_URL])
        db = queries._engine.raw_connection()
        with app.open_resource(CreateDb, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()    
    
@app.route('/', methods=['GET'])
def home():
    return '''<h1>SPOTIFY, but without music streaming</h1>
    <h2>TRACKS MICROSERVICE</h2>
<p>A prototype API for delivering track, playlist, and user data.</p>'''

@app.route('/api/resources/tracks/all', methods=['GET'])
def all_tracks():
    #all_tracks = queries.all_tracks()
    #queries1.connect(app.config['TRACKS_ONE'])
    #all_tracks.append(queries1.all_tracks())
    #queries2.connect(app.config['TRACKS_TWO'])
    #all_tracks.append(queries2.all_tracks())
    #queries3.connect(app.config['TRACKS_THREE'])
    #all_tracks.append(queries3.all_tracks())
    #return list(None)
    #return None
    #tracks = []
    #queries3.connect(app.config['TRACKS_THREE'])
    #dictA = queries3.all_tracks()
    #queries1.connect(app.config['TRACKS_ONE'])
    #dictB = queries1.all_tracks()
    #merged_dict = {**json.loads(dictA), **json.loads(dictB)}
    #s1 = json.dumps(merged_dict)
    #return list(s1)
    all_tracks = queries.all_tracks()
    return list(all_tracks)
#GET track that matches id number
@app.route('/api/resources/tracks/<string:id>', methods=['GET'])
def track(id):
    if int(id) % 3 == 0:
        queries1.connect(app.config['TRACKS_ONE'])
        return queries1.create_track(**track)
    elif id % 3 == 1:
        queries2.connect(app.config['TRACKS_TWO'])
        return queries2.create_track(**track)
    elif int(id) % 3 == 2:
        queries3.connect(app.config['TRACKS_THREE'])
        return queries3.create_track(**track)  

@app.route('/api/resources/tracks', methods=['GET', 'POST'])
def tracks():
    if request.method == 'GET':
        return filter_tracks(request.args)
        #return test_id()
    elif request.method == 'POST':
        return create_track_v2(request.data)

@app.route('/api/resources/tracks/update', methods=['GET','PUT'])
def updates():
    if request.method == 'GET':
        return (list(queries.all_tracks())) 
    if request.method == 'PUT':
        return update_track(request.data)   
        
@app.route('/api/resources/tracks/delete/<string:id>', methods=['GET','DELETE'])
def deletes(id):
    if request.method =='GET':
        return (list(queries.all_tracks())) 
    if request.method == 'DELETE':
        return delete_track(id)
        
def delete_track(id):
    track_to_delete = id
    filter_query =[]
    try:
        query = "DELETE FROM tracks WHERE id=?"
        filter_query.append(track_to_delete)
        queries._engine.execute(query,filter_query)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NO_CONTENT
    return '', status.HTTP_204_NO_CONTENT

#When posting to flask api, erase trailing whitespaces,
#{"title":"Blue Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s24","arturl":"C;//song/img/s24"},{"title":"Yellow Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s23","arturl":"C;//song/img/s23"}
#{"title":"Yellow Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s23"}
def create_track(track):
    track = request.data
    required_fields = ['title', 'album', 'artist', 'duration','url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        track['id'] = queries.create_track(**track)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
        
    return track, status.HTTP_201_CREATED

def test_id():
    trackid = uuid.uuid4()
    track = {'id':int(trackid)%3}
    return track,status.HTTP_201_CREATED  
def create_track_v2(track):
    track = request.data
    required_fields = ['title', 'album', 'artist', 'duration','url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        trackid = uuid.uuid4()
        modVal = int(trackid) % 3
        track['id'] = str(trackid)
       # queries.create_track(**track)        

        if str(modVal % 3) == '0':
            queries1.connect(app.config['TRACKS_ONE'])
            queries1.create_track(**track)
        elif str(modVal % 3 )== '1':
            queries2.connect(app.config['TRACKS_TWO'])
            queries2.create_track(**track)
        elif str(modVal % 3) == '2':
            queries3.connect(app.config['TRACKS_THREE'])
            queries3.create_track(**track)
    
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED
    
#PUT Method - Requires 'id' or 'artist title'
def update_track(track):
    search_by_id = ['columnName','columnValue','id']
    track = request.data
    to_filter = []
    
    if 'changeColumn' in track and 'changeValueTo' in track and 'id' in track:
        modVal = id % 3
        columnName = track['changeColumn']
        query = "UPDATE tracks SET {}=? WHERE id =?".format(columnName)
        to_filter.append(track['changeValueTo'])
        to_filter.append(track['id'])
        if str(modVal % 3) == '0':
            queries1.connect(app.config['TRACKS_ONE'])
            queries1._engine.execute(query,to_filter)
        elif str(modVal % 3 )== '1':
            queries2.connect(app.config['TRACKS_TWO'])
            queries2._engine.execute(query,to_filter)
        elif str(modVal % 3) == '2':
            queries3.connect(app.config['TRACKS_THREE'])
            queries3._engine.execute(query,to_filter)
    return track, status.HTTP_201_CREATED   

 
#Search for track based off given parameter
def filter_tracks(query_parameters):
    id = query_parameters.get('id')
    title = query_parameters.get('title')
    album = query_parameters.get('album')
    artist = query_parameters.get('artist')

    
    query = "SELECT * FROM tracks WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if album:
        query += ' album=? AND'
        to_filter.append(album) 
    if not (id or title or album or artist):
        raise exceptions.NotFound()
    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()
    #one = results['title']
    #return results
    #return list(results)
    return list(map(dict, results))
    

