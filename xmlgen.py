#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql
import requests
import json
#import xml.etree.ElementTree as ET
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
    r = requests.get('http://localhost:8000/playlist/playlist/all')
    json = r.json()
    print (json)
    return '''<h1>SPOTIFY, but without music streaming</h1>
    <h2>XML GENERATOR MICROSERVICE</h2>
<p>A prototype API for delivering playlist data in an XML format</p>'''
    #r = requests.get('http://localhost:5000/playlist/all')
    #json = r.json()
    #print json

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

#test function, delete later
@app.route('/test',methods=['GET'])
def select_playlist():
    payload = {'id':1}
    r = requests.get('http://localhost:8000/playlist/playlist/display', params=payload)
    json = r.json()
    print ('I love anime!!!')
    print (json)
    from xml.etree import ElementTree
    mystring = "START OF XML:<root><a>1</a></root>" + "\r\r\n"
    root = ElementTree.fromstring(mystring)
    ElementTree.dump(root)
    return json

#test function, delete later
@app.route('/test/<int:id>',methods=['GET'])
def select_playlist2(id):
    payload = {'id':id}
    r = requests.get('http://localhost:8000/playlist/playlist/select', params=payload)
    json = r.json()
    return json

#Generates an XML file given a playlist ID
@app.route('/getxml/<int:id>',methods=['GET'])
def get_xml(id):

    #Var Declarations
    payload = {'id':id}
    outputString = "Playlist id: " + str(id) + "\r\r\n"
    outputStringXML = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\r\n<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\">\r\r\n\t<title>"+ str(id) + "</title>\r\r\n\t<trackList>\r\r\n"
    #Requests into json into dict objs
    songsInPlaylist = requests.get('http://localhost:8000/playlist/playlist/display', params=payload)
    songsInPlaylistJSON = songsInPlaylist.json()
    #songsInPlaylistDict = json.loads(songsInPlaylistJSON)

    playlistInfo = requests.get('http://localhost:8000/playlist/playlist/select', params=payload)
    #playlistInfoJSON = playlistInfo.json() <--- Unknown error cause
    #playlistInfoJSON = json.loads(playlistInfo.text)

    allSongs = requests.get('http://localhost:8000/tracks/api/resources/tracks/all')
    allSongsJSON = allSongs.json()
    #allSongsDict = json.loads(allSongsJSON)

    #Loop through songs in playlist
    for myArray in songsInPlaylistJSON:
        outputString += "Track: " + str(myArray['track_id']) + "\r\r\n"
        outputStringXML += "\t\t<track>\r\r\n"
        #outputStringXML += "\t\t\t<location>" + INSERTTRACKLOCATIONHERE + "</location>\r\r\n"
        
        #Find that song in the list of all songs
        for myArray2 in allSongsJSON:
            if str(myArray['track_id']) == str(myArray2['id']):
                outputString += "Title: " + str(myArray2['title']) + "\r\r\n"
                outputString += "Artist: " + str(myArray2['artist']) + "\r\r\n"
                outputString += "Album: " + str(myArray2['album']) + "\r\r\n"
                outputString += "URL: " + str(myArray2['url']) + "\r\r\n"

                outputStringXML += "\t\t\t<location> " + str(myArray2['url']) + "</location>\r\r\n"
                outputStringXML += "\t\t\t<title>" + str(myArray2['title']) + "</title>\r\r\n"
                outputStringXML += "\t\t\t<creator>" + str(myArray2['artist']) + "</creator>\r\r\n"
                outputStringXML += "\t\t\t<album> " + str(myArray2['album']) + "</album>\r\r\n"

        outputStringXML += "\t\t</track>\r\r\n"

    #return outputString + "\r\r\n\r\r\n" + outputStringXML + "\t</tracklist>\r\r\n</playlist>END OF XML"
    #return outputStringXML + "\t</tracklist>\r\r\n</playlist>END OF XML"
    
    outputStringXML += "\t</trackList>\r\r\n</playlist>"
    from xml.etree import ElementTree
    root = ElementTree.fromstring(outputStringXML)
    #ElementTree.dump(root)
    myfile = open("test.xml","w+")
    myfile.write(outputStringXML)
    return outputString

