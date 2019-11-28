#from flask import Flask, jsonify
#app = Flask(__name__)

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
    return '''<h1>Descriptions Microservice</h1>'''

@app.route('/api/resources/descriptions', methods=['GET', 'POST'])
def descriptions():
    if request.method == 'GET':
        return get_desc(request.args)
       # return get_description(request.args)
    elif request.method == 'POST':
        return create_description(request.data)
        
def get_desc(params):
    id = params.get('id')
    to_filter = []
    to_filter.append(id)
    query = "SELECT * FROM descriptions WHERE id=?"
    results = queries._engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))
    
def get_description():
    get_description = queries.descriptions()
    return list(get_descriptions)

def create_description(description):
    description = request.data
    required_fields = ['description', 'username', 'url']

    if not all([field in description for field in required_fields]):
        raise exceptions.ParseError()
    try:
        description['id'] = queries.create_description(**description)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return description, status.HTTP_201_CREATED
