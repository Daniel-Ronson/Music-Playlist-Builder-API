#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql

from werkzeug.security import generate_password_hash,check_password_hash


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
<p>USERS MICROSERViCE</p>'''

@app.route('/api/resources/user', methods=['GET'])
def user():
    if request.method == 'GET':
        query_paramenrs = request.args


@app.route('/api/resources/users/all', methods=['GET'])
def all_users():
    all_users = queries.all_users()
    return list(all_users)

#GET user that matches id number
@app.route('/api/resources/users/<int:id>', methods=['GET'])
def one_user(id):
    return queries.user_by_id(id=id)

@app.route('/api/resources/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return filter_users(request.args)
    elif request.method == 'POST':
        return create_user(request.data)

@app.route('/api/resources/users/update', methods=['GET','PUT'])
def updates():
    if request.method == 'GET':
        return (list(queries.all_users()))
    if request.method == 'PUT':
        return update_user(request.data)

@app.route('/api/resources/users/delete/<int:id>', methods=['GET','DELETE'])
def deletes(id):
    if request.method =='GET':
        return (list(queries.all_users()))
    if request.method == 'DELETE':
        return delete_user(id)

def delete_user(id):
    user_to_delete = id
    filter_query =[]
    try:
        query = "DELETE FROM users WHERE id=?"
        filter_query.append(user_to_delete)
        queries._engine.execute(query,filter_query)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NO_CONTENT
    return '', status.HTTP_204_NO_CONTENT


#{"username": "ausername", "password": "abc123","firstname": "Daniel","lastname": "Ronson","email": "aemail@hotmail.com","id": 2}
def create_user(user):
    user = request.data
    required_fields = ['username', 'password', 'firstname', 'lastname','email']
    username = user['username']
    password = user['password']

#To check username and password matching
    if not all([field in user for field in required_fields]):
        return authenticate_user(username,password)

    firstname = user['firstname']
    lastname = user['lastname']
    email = user['email']
    hashed_password = generate_password_hash(password)
    query ="INSERT INTO users(username, password, firstname, lastname, email) VALUES('"+username+"','"+hashed_password+"', '"+firstname+"', '"+lastname+"', ? );"
    to_filter = []
    to_filter.append(email)
    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        queries._engine.execute(query, to_filter)
        #user['id'] = queries.create_user(**user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return user, status.HTTP_201_CREATED

def update_user(user):
    search_by_id = ['columnName','columnValue','id']
    search_by_unique_constraint = ['columnName','columnValue','hashed_password']
    user = request.data
    to_filter = []

    if 'changeColumn' in user and 'changeValueTo' in user and 'hashed_password' in user:
        hashed_password = user['hashed_password']
        columnName = user['changeColumn']
        columnValue =user['changeValueTo']
        query = "UPDATE users SET {}=? WHERE hashed_password=?".format(columnName)
        to_filter.append(columnValue)
        to_filter.append(hashed_password)
        queries._engine.execute(query,to_filter)

    elif 'id' in user and 'username' in user:
        columnName = user['changeColumn']
        columnValue = hashed_password['changeValueTo']
        id = user['id']
        queries._engine.execute("UPDATE users SET %s=? WHERE id=?" % (columnName,),(columnValue,id))
    return user, status.HTTP_201_CREATED

def authenticate_user(username,password):
    query = "SELECT password FROM user WHERE username=?;"
    to_filter= []
    to_filter.append(username)
    results = query_db(query, to_filter).fetch_all
    if not results:
        return jsonify(message="User Authentication unsuccessful. Try with new password"),401

    authenticated = check_password_hash(results[0]['hashed_password'],password)
    if authenticated:
        return jsonify(message="User Authentication successful"),200

    return jsonify(message="User Authentication unsuccessful. Try with new password"),401

    return list(map(dict, results))

#Search for users based off given parameter
def filter_users(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    hashed_password = query_parameters.get('hashed_password')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if username and password:
        return authenticate_user(username,password)

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if hashed_password:
        query += ' hashed_password=? AND'
        to_filter.append(hashed_password)
    if not (id or username or hashed_password):
        raise exceptions.NotFound()
    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))
