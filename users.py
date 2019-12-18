#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql

from werkzeug.security import generate_password_hash,check_password_hash

from cassandra.cluster import Cluster
from cassandra import ReadTimeout
cluster = Cluster(['172.17.0.2'],port=9042)
session = cluster.connect() 
session.execute('USE Music')

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')


#delete playlist based off email and playlistname
@app.route('/users/create',methods=['GET','POST'])
def create_user_service():
    if request.method == 'GET':
        return get_all_users()
    if request.method == 'POST':
        return filter_create_user(request.data)
     
def filter_create_user(user):
    username = user['username']
    firstname = user['firstname']
    lastname = user['lastname']
    email = user['email']
    password = user['password']    
    hashed_password = generate_password_hash(password)
    sql = "INSERT INTO users (username,firstname,lastname,email,password) VALUES (%s,%s,%s,%s,%s)"
    
    try:
        session.execute(sql,(username,firstname,lastname,email,hashed_password))
        return playlist, status.HTTP_201_CREATED
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    
    
#select one user by email
#?email=e@gmail.com
@app.route('/users/select', methods=['GET'])
def retrieve_users():
    return get_one_users(request.args)
        
def get_one_users(user):
    email = user.get('email')
    query = "SELECT * FROM users WHERE email= %s ALLOW FILTERING"
    res = session.execute_async(query, (email,))
    row_array = []
    
    try:
        rows = res.result()
        item = rows[0]
        user =  {"username":item.username,"email":item.email, "firstname": item.firstname,"lastname": item.lastname,"descriptionlist":str(item.description)}
        row_array.append(user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return list(row_array)
 
#{"email":"e@gmail.com","password":"pass"}
@app.route('/users/authenticate', methods=['GET','POST'])
def authenticate_users_service():
    if request.method == 'GET':
        return get_all_users()
    elif request.method == 'POST':
        return authenticate(request.data)
    
def authenticate(data):
    check_password = data['password']
    email = data['email']
    
    user_data = get_one_users_password(email)
    hashed_password = user_data[0]['password']
    var = check_password_hash(hashed_password,check_password)
    if var:
        return_message = {'Correct Password' : 'TRUE' , 'Username' :user_data[0]['username']}
        return return_message, status.HTTP_200_OK
    
    return_message = {'Correct Password' : 'FALSE' , 'Username' :user_data[0]['username']}    
    return return_message, status.HTTP_200_OK 
    
def get_one_users_password(email):
    email = email
    query = "SELECT username, password FROM users WHERE email= %s ALLOW FILTERING"
    res = session.execute_async(query, (email,))
    row_array = []
    
    try:
        rows = res.result()
        item = rows[0]
        user =  {"username":item.username,"password":item.password}
        row_array.append(user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NOT_FOUND   
    return list(row_array)
    

#change password
#{"changeValueTo":"asd","email" : "e@gmail.com", "password":"pass"}
@app.route('/users/update', methods=['GET','PUT'])
def users_updates_service():
    if request.method == 'GET':
        return get_all_users()
    if request.method == 'PUT':
        return update_users(request.data) 
        
def update_users(user):

    authentication_data = authenticate(user)
    is_valid_password = bool(authentication_data[0]['Correct Password'])

    if is_valid_password:
        changeValueTo = user['changeValueTo']
        hashed_password = generate_password_hash(changeValueTo)
        email = user['email']            
        query_update_track = "UPDATE users SET password = %s WHERE email=%s"
        session.execute_async(query_update_track,(hashed_password,email))

    return user, status.HTTP_201_CREATED   
   
   
#GET all users
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
 
 
#delete user based off email
@app.route('/users/delete',methods=['GET','DELETE'])
def delete_user_service():
    if request.method == 'GET':
        return get_all_users()
    if request.method == 'DELETE':
        return filter_delete_user(request.data)
     
def filter_delete_user(data):
    email = data['email']
    query = "DELETE FROM users WHERE email= %s "
    
    session.execute_async(query, (email,))         
    return '', status.HTTP_204_NO_CONTENT 
  
 
    
@app.route('/', methods=['GET'])
def home():
    return '''<h1>SPOTIFY, but without music streaming</h1>
<p>USERS MICROSERViCE</p>'''
