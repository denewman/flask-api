from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
import sqlite3
import os

#from models import *

app = Flask(__name__)
api = Api(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response
  
class subscription(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('subscriptionName', type=str, help='Subscription name to create subscription')
            parser.add_argument('destinationGroupName', type=str, help='Destination group to create subscription')
            parser.add_argument('sensorName', type=str, help='Sensor Name to create subscription')
            parser.add_argument('subscriptionInterval', type=float, help='Interval for the new subscription')
            args = parser.parse_args()

            _subscriptionName = args['subscriptionName']
            _destinationGroupName = args['destinationGroupName']
            _sensorName = args['sensorName']
            _subscriptionInterval = args['subscriptionInterval']

            db = get_db()
            cursor = db.execute('INSERT INTO subscription (subscriptionName, destinationGroupName, sensorName, subscriptionInterval) values (?, ?, ?, ?)',
                [_subscriptionName, _destinationGroupName, _sensorName, _subscriptionInterval])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'subscription': {'subscriptionName': _subscriptionName,'destinationGroupName': _destinationGroupName, 'sensorName': _sensorName, 'subscriptionInterval': _subscriptionInterval}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT subscriptionName, destinationGroupName, sensorName, subscriptionInterval FROM subscription ORDER BY subscriptionName desc')
            data = cursor.fetchall()
	
            subscription_list = []
            for subsciption in data:
                i = {
                    'subscriptionName': subsciption[0],
                    'destinationGroupName': subsciption[1],
                    'sensorName': subsciption[2],
                    'subscriptionInterval': subscription[3]
                }
                subscription_list.append(i)
	
            return {'Status Code': '200', 'subscription': subscription_list}
	
        except Exception as e:
            return {'error': str(e)}

class destinationGroup(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('destinationGroupName', type=str, help='')
            parser.add_argument('destinationGroupAddress', type=str, help='')
            parser.add_argument('destinationGroupPort', type=str, help='')
            parser.add_argument('destinationGroupEncoding', type=str, help='')
            parser.add_argument('destinationGroupProtocol', type=str, help='')
            args = parser.parse_args()

            _destinationGroupName = args['destinationGroupName']
            _destinationGroupAddress = args['destinationGroupAddress']
            _destinationGroupPort = args['destinationGroupPort']
            _destinationGroupEncoding = args['destinationGroupEncoding']
            _destinationGroupProtocol = args['destinationGroupProtocol']

            db = get_db()
            cursor = db.execute('INSERT INTO destinationGroup (destinationGroupName, destinationGroupAddress, destinationGroupPort, destinationGroupEncoding, destinationGroupProtocol) values (?, ?, ?, ?, ?)',
                [_destinationGroupName, _destinationGroupAddress, _destinationGroupPort, _destinationGroupEncoding, _destinationGroupProtocol])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {
					'destinationGroup': {
						'destinationGroupName': _destinationGroupName,
						'destinationGroupAddress': _destinationGroupAddress,
						'destinationGroupPort': _destinationGroupPort,
						'destinationGroupEncoding': _destinationGroupEncoding,
						'destinationGroupProtocol': _destinationGroupProtocol
						}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT subscriptionName, destinationGroupName, sensorName, subscriptionInterval FROM subscription ORDER BY subscriptionName desc')
            data = cursor.fetchall()
	
            destinationGroup_list = []
            for destinationGroup in data:
                i = {
                    'subscriptionName': destinationGroup[0],
                    'destinationGroupName': destinationGroup[1],
                    'sensorName': destinationGroup[2],
                    'subscriptionInterval': destinationGroup[3]
                }
                destinationGroup_list.append(i)
	
            return {'Status Code': '200', 'destinationGroup': destinationGroup_list}
	
        except Exception as e:
            return {'error': str(e)}
    
class sensor(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('sensorName', type=str, help='Sensor Name and primary key')
            args = parser.parse_args()

            _sensorName = args['sensorName']

            db = get_db()
            cursor = db.execute('INSERT INTO sensor (sensorName) values (?)',
                [_sensorName])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'sensor': {'sensorName': _sensorName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute('SELECT sensorName FROM sensor ORDER BY sensorName')
            data = cursor.fetchall()
	
            sensor_list = []
            for sensor in data:
                i = {
                    'sensorName': sensor[0],
                }
                sensor_list.append(i)
	
            return {'Status Code': '200', 'sensor': sensor_list}
	
        except Exception as e:
            return {'error': str(e)}

api.add_resource(subscription, '/subscription')
api.add_resource(destinationGroup, '/destinationGroup')
api.add_resource(sensor, '/sensor')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

