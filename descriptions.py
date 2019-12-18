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

#GET: give email, track name, track artist 
#Post: give email, track name, track artist 
# {"email": "e@gmail.com","artist":"Led Zeppelin","title":"The Song Remains The Same","description":"this song rocks"}
@app.route('/user/descriptions/add', methods=['GET','PUT'])
def add_track_to_playlist():
    if request.method == 'GET':
        return get_all_users()
    if request.method =='PUT':
        return user_add_description(request.data)

def user_add_description(data):
    email = data['email']
    title = data['title']
    artist = data['artist']
    description = data['description']
    track_data = filter_select_track_for_description(title,artist)
    uuid = track_data[0]['uuid']
    query_update_track = "UPDATE users SET description = description + {%s : %s} WHERE email =%s"
    session.execute_async(query_update_track,(uuid,description,email))
    #message = {'ok':'ok'}
    return data, status.HTTP_201_CREATED
 

 # ?email=e@gmail.com
#{"email": "e@gmail.com","artist":"Led Zeppelin","title":"The Song Remains The Same","description":"this song rocks"}
@app.route('/users/get/description', methods=['GET'])
def get_description_service():
    if request.method == 'GET':
        return retrieve_description(request.args)



     
#get all users descriptions for tracks
def retrieve_description(email_data):
    
    email = email_data.get('email')
    query = "SELECT description FROM users WHERE email = %s ALLOW FILTERING"
    res = session.execute_async(query, (email,))
    row_array = []
    
    try:
        rows = res.result()
        item = rows[0]
        description =  {"description":str(item.description)}
        row_array.append(description)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return list(row_array) 


    
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Descriptions Microservice</h1>'''
    
#GET all users
#placeholder function, not required 
@app.route('/users/all', methods=['GET'])
def all_users():
    return get_all_users()
    
def get_all_users():
    user_container = []
    rows = session.execute('SELECT * from users')
    for item in rows:
        user =  {"username":item.username,"email":item.email, "firstname": item.firstname,"lastname": item.lastname,"descriptionlist":str(item.description)}
        user_container.append(user)
    return list(user_container)
