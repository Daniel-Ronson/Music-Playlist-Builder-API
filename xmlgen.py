#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql
import requests
import json
from xml.etree import ElementTree
#import xml.etree.ElementTree as ET
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])
from cassandra import ReadTimeout
from cassandra.cluster import Cluster
cluster = Cluster(['172.17.0.2'],port=9042)
session = cluster.connect() 
session.execute('USE Music')

from pymemcache.client import base

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
    #json = r.json()
    print (json)
    return '''<h1>SPOTIFY, but without music streaming</h1>
    <h2>XML GENERATOR MICROSERVICE</h2>
<p>A prototype API for delivering playlist data in an XML format</p>'''
    #r = requests.get('http://localhost:5000/playlist/all')
    #json = r.json()
    #print json


#test function, delete later
@app.route('/test',methods=['GET'])
def select_playlist():
    payload = {'id':1}
    r = requests.get('http://localhost:8000/playlist/playlist/display', params=payload)
    json = r.json()
    print ('I love anime!!!')
    print (json)
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
@app.route('/getxml',methods=['GET'])
def get_xcspf_service():
    return get_xml()
    
def get_xml():
    
    #email = query_parameters.get('email')
    #playlistname = query_parameters.get('playlistname')
     
    client = base.Client(('localhost', 11211)) #Declare the memcache object here
    # Key is string email concat to string playlistname
    payload = {'email':'e@gmail.com','playlistname':'tunes'}
    outputString = ""
    
    key = payload['email'] + payload['playlistname']

    #Check cache for data
    memcacheresult = client.get(key)

    if memcacheresult is None: #If data is not found, generate xml string, and store into cache

        outputString += "Data not found! Calling microservices.\r\r\nPlaylist id: " + "\r\r\n"

        #GET list of song's uuid
        songsInPlaylist = requests.get('http://localhost:8000/playlist/playlist/select/tracks', params=payload)
        songsInPlaylistJSON = songsInPlaylist.json() #list of songs
    
        #get track info: title, artist, album
        #get track data from uuid  
        #        outputString += "Track: " + str(track) + "\r\r\n"
        outputStringXML = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\r\n<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\">\r\r\n\t<title>"+ "playlist" + "</title>\r\r\n\t<trackList>\r\r\n"

        for track in songsInPlaylistJSON:
            payload = {'id' : track }
            trackData = requests.get('http://localhost:8000/tracks/get/track/id', params=payload)
            trackDataJSON = trackData.json()
            outputString += "Title: " + str(trackDataJSON[0]['title']) + "\r\r\n"
            outputString += "Artist: " + str(trackDataJSON[0]['artist']) + "\r\r\n"
            outputString += "Album: " + str(trackDataJSON[0]['album']) + "\r\r\n"
            outputString += "URL: " + str(trackDataJSON[0]['url']) + "\r\r\n"
            outputStringXML += "\t\t<track>\r\r\n"
            outputStringXML += "\t\t\t<location> " + str(trackDataJSON[0]['url']) + "</location>\r\r\n"
            outputStringXML += "\t\t\t<title>" + str(trackDataJSON[0]['title']) + "</title>\r\r\n"
            outputStringXML += "\t\t\t<creator>" + str(trackDataJSON[0]['artist']) + "</creator>\r\r\n"
            outputStringXML += "\t\t\t<album> " + str(trackDataJSON[0]['album']) + "</album>\r\r\n"
            outputStringXML += "\t\t</track>\r\r\n"
        
        outputStringXML += "\t</trackList>\r\r\n</playlist>"

        #client.set(key,outputStringXML)
        #set(key, value, expire=0, noreply=None, flags=None)
        client.set(key,outputStringXML,9001)
        #client.set(key,outputStringXML,9001,true,0)

    else:
        outputStringXML = memcacheresult
        outputString += "Data in cache found!\r\r\n"

    from xml.etree import ElementTree

    root = ElementTree.fromstring(outputStringXML)
    myfile = open("test.xml","w+")
    myfile.write(outputStringXML)
    return outputString
