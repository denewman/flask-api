from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
import sqlite3
import os

# from models import *

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
            cursor = db.execute(
                'INSERT INTO subscription (subscriptionName, destinationGroupName, sensorName, subscriptionInterval) VALUES (?, ?, ?, ?)',
                [_subscriptionName, _destinationGroupName, _sensorName, _subscriptionInterval])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'subscription': {'subscriptionName': _subscriptionName,
                                         'destinationGroupName': _destinationGroupName, 'sensorName': _sensorName,
                                         'subscriptionInterval': _subscriptionInterval}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT subscriptionName, destinationGroupName, sensorName, subscriptionInterval FROM subscription ORDER BY subscriptionName DESC')
            data = cursor.fetchall()

            subscription_list = []
            for subscription in data:
                i = {
                    'subscriptionName': subscription[0],
                    'destinationGroupName': subscription[1],
                    'sensorName': subscription[2],
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
            cursor = db.execute(
                'INSERT INTO destinationGroup (destinationGroupName, destinationGroupAddress, destinationGroupPort, destinationGroupEncoding, destinationGroupProtocol) VALUES (?, ?, ?, ?, ?)',
                [_destinationGroupName, _destinationGroupAddress, _destinationGroupPort, _destinationGroupEncoding,
                 _destinationGroupProtocol])
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
            cursor = db.execute(
                'SELECT destinationGroupName, destinationGroupAddress, destinationGroupPort, destinationGroupEncoding, destinationGroupProtocol FROM destinationGroup ORDER BY destinationGroupName DESC')
            data = cursor.fetchall()

            destinationGroup_list = []
            for destinationGroup in data:
                i = {
                    'destinationGroupName': destinationGroup[0],
                    'destinationGroupAddress': destinationGroup[1],
                    'destinationGroupPort': destinationGroup[2],
                    'destinationGroupEncoding': destinationGroup[3],
                    'destinationGroupProtocol': destinationGroup[4]
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
            parser.add_argument('sensorPaths', action='append')
            args = parser.parse_args()

            _sensorName = args['sensorName']
            _sensorPaths = args['sensorPaths']

            db = get_db()
            cursor = db.execute('INSERT INTO sensor (sensorName) VALUES (?)',
                                [_sensorName])
            data = cursor.fetchall()

            for sensorPath in _sensorPaths:
                cursor1 = db.execute('INSERT INTO linkSensorPath (sensorName, sensorPathName) VALUES (?, ?)',
                                     [_sensorName, sensorPath])
                data1 = cursor1.fetchall()
                if len(data1) is 0:
                    db.commit()

            if len(data) is 0:
                db.commit()
                return {'sensor': {'sensorName': _sensorName, 'sensorPaths': _sensorPaths}}
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
                cursor1 = db.execute('SELECT sensorPathName FROM linkSensorPath WHERE sensorName=?', (sensor[0],))
                data1 = cursor1.fetchall()

                path_list = []
                for path in data1:
                    j = path[0]
                    path_list.append(j)

                i = {
                    'sensorName': sensor[0],
                    'sensorPath': path_list
                }
                sensor_list.append(i)

            return {'Status Code': '200', 'sensor': sensor_list}

        except Exception as e:
            return {'error': str(e)}


class policyGroup(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyGroupName', type=str, help='Policy Group name to create policy')
            parser.add_argument('collectorName', type=str, help='collector name to create policy')
            parser.add_argument('policyName', type=str, help='policy name to create policy')
            args = parser.parse_args()

            _policyGroupName = args['policyGroupName']
            _collectorName = args['collectorName']
            _policyName = args['policyName']

            db = get_db()
            cursor = db.execute(
                'INSERT INTO policyGroup (policyGroupName, collectorName, policyName) VALUES (?, ?, ?)',
                [_policyGroupName, _collectorName, _policyName])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'policyGroup': {'policyGroupName': _policyGroupName,
                                        'collectorName': _collectorName,
                                        'policyName': _policyName}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT policyGroupName, collectorName, policyName FROM policyGroup ORDER BY policyGroupName DESC')
            data = cursor.fetchall()

            policyGroup_list = []
            for policyGroup in data:
                i = {
                    'policyGroupName': policyGroup[0],
                    'collectorName': policyGroup[1],
                    'policyName': policyGroup[2]
                }
                policyGroup_list.append(i)

            return {'Status Code': '200', 'policyGroup': policyGroup_list}

        except Exception as e:
            return {'error': str(e)}


class collector(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('collectorName', type=str, help='')
            parser.add_argument('collectorAddress', type=str, help='')
            parser.add_argument('collectorEncoding', type=str, help='')
            parser.add_argument('collectorPort', type=str, help='')
            parser.add_argument('collectorProtocol', type=str, help='')
            args = parser.parse_args()

            _collectorName = args['collectorName']
            _collectorAddress = args['collectorAddress']
            _collectorEncoding = args['collectorEncoding']
            _collectorPort = args['collectorPort']
            _collectorProtocol = args['collectorProtocol']

            db = get_db()
            cursor = db.execute(
                'INSERT INTO collector (collectorName, collectorAddress, collectorEncoding, collectorPort, collectorProtocol) VALUES (?, ?, ?, ?, ?)',
                [_collectorName, _collectorAddress, _collectorEncoding, _collectorPort,
                 _collectorProtocol])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {
                    'collector': {
                        'collectorName': _collectorName,
                        'collectorAddress': _collectorAddress,
                        'collectorEncoding': _collectorEncoding,
                        'collectorPort': _collectorPort,
                        'collectorProtocol': _collectorProtocol
                    }}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT collectorName, collectorAddress, collectorEncoding, collectorPort, collectorProtocol FROM collector ORDER BY collectorName DESC')
            data = cursor.fetchall()

            collector_list = []
            for collector in data:
                i = {
                    'collectorName': collector[0],
                    'collectorAddress': collector[1],
                    'collectorEncoding': collector[2],
                    'collectorPort': collector[3],
                    'collectorProtocol': collector[4]
                }
                collector_list.append(i)

            return {'Status Code': '200', 'collector': collector_list}

        except Exception as e:
            return {'error': str(e)}


class policy(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyName', type=str, help='')
            parser.add_argument('policyDescription', type=str, help='')
            parser.add_argument('policyComment', type=str, help='')
            parser.add_argument('policyIdentifier', type=str, help='')
            parser.add_argument('policyPeriod', type=float, help='')
            args = parser.parse_args()

            _policyName = args['policyName']
            _policyDescription = args['policyDescription']
            _policyComment = args['policyComment']
            _policyIdentifier = args['policyIdentifier']
            _policyPeriod = args['policyPeriod']

            db = get_db()
            cursor = db.execute(
                'INSERT INTO policy (policyName, policyDescription, policyComment, policyIdentifier, policyPeriod) VALUES (?, ?, ?, ?, ?)',
                [_policyName, _policyDescription, _policyComment, _policyIdentifier,
                 _policyPeriod])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {
                    'policy': {
                        'policyName': _policyName,
                        'policyDescription': _policyDescription,
                        'policyComment': _policyComment,
                        'policyIdentifier': _policyIdentifier,
                        'policyPeriod': _policyPeriod
                    }}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT policyName, policyDescription, policyComment, policyIdentifier, policyPeriod FROM policy ORDER BY policyName DESC')
            data = cursor.fetchall()

            policy_list = []
            for policy in data:
                i = {
                    'policyName': policy[0],
                    'policyDescription': policy[1],
                    'policyComment': policy[2],
                    'policyIdentifier': policy[3],
                    'policyPeriod': policy[4]
                }
                policy_list.append(i)

            return {'Status Code': '200', 'policy': policy_list}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(subscription, '/subscription')
api.add_resource(destinationGroup, '/destinationGroup')
api.add_resource(sensor, '/sensor')
api.add_resource(policyGroup, '/policyGroup')
api.add_resource(collector, '/collector')
api.add_resource(policy, '/policy')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True, threaded=True)
