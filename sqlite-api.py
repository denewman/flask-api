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
            db.execute('PRAGMA foreign_keys=ON')
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

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM subscription')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singleSubscription(Resource):
    def delete(self, subscriptionName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM subscription WHERE subscriptionName=?', (subscriptionName,))
            db.commit()
            return {'Status Code': '200'}

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

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM destinationGroup')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singleDestinationGroup(Resource):
    def delete(self, destinationGroupName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM destinationGroup WHERE destinationGroupName=?', (destinationGroupName,))
            db.commit()
            return {'Status Code': '200'}

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
            db.execute('PRAGMA foreign_keys=ON')
            cursor = db.execute('SELECT sensorName FROM sensor ORDER BY sensorName')
            data = cursor.fetchall()

            sensor_list = []
            for sensor in data:
                cursor1 = db.execute('SELECT sensorPathName FROM linkSensorPath WHERE sensorName=?', (sensor[0],))
                data1 = cursor1.fetchall()

                path_list = []
                for path in data1:
                    path_list.append(path[0])

                i = {
                    'sensorName': sensor[0],
                    'sensorPath': path_list
                }
                sensor_list.append(i)

            return {'Status Code': '200', 'sensor': sensor_list}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkSensorPath')
            db.execute('DELETE FROM sensor')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singleSensor(Resource):
    def delete(self, sensorName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkSensorPath WHERE sensorName=?', (sensorName,))
            db.execute('DELETE FROM sensor WHERE sensorName=?', (sensorName,))
            db.commit()
            return {'Status Code': '200'}

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
            db.execute('PRAGMA foreign_keys=ON')
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

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM policyGroup')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singlePolicyGroup(Resource):
    def delete(self, policyGroupName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM policyGroup WHERE policyGroupName=?', (policyGroupName,))
            db.commit()
            return {'Status Code': '200'}

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

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM collector')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singleCollector(Resource):
    def delete(self, collectorName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM collector WHERE collectorName=?', (collectorName,))
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class policy(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyName', type=str, help='')
            parser.add_argument('policyVersion', type=float, help='')
            parser.add_argument('policyDescription', type=str, help='')
            parser.add_argument('policyComment', type=str, help='')
            parser.add_argument('policyIdentifier', type=str, help='')
            parser.add_argument('policyPeriod', type=float, help='')
            parser.add_argument('policyPaths', action='append')
            args = parser.parse_args()

            _policyName = args['policyName']
            _policyVersion = args['policyVersion']
            _policyDescription = args['policyDescription']
            _policyComment = args['policyComment']
            _policyIdentifier = args['policyIdentifier']
            _policyPeriod = args['policyPeriod']
            _policyPaths = args['policyPaths']

            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            cursor = db.execute(
                'INSERT INTO policy (policyName, policyVersion, policyDescription, policyComment, policyIdentifier, policyPeriod) VALUES (?, ?, ?, ?, ?, ?)',
                [_policyName, _policyVersion, _policyDescription, _policyComment, _policyIdentifier, _policyPeriod])
            data = cursor.fetchall()

            for policyPath in _policyPaths:
                cursor1 = db.execute('INSERT INTO linkPolicyPath (policyName, policyPathName) VALUES (?, ?)',
                                     [_policyName, policyPath])
                data1 = cursor1.fetchall()
                if len(data1) is 0:
                    db.commit()

            if len(data) is 0:
                db.commit()
                return {
                    'policy': {
                        'policyName': _policyName,
                        'policyVersion': _policyVersion,
                        'policyDescription': _policyDescription,
                        'policyComment': _policyComment,
                        'policyIdentifier': _policyIdentifier,
                        'policyPeriod': _policyPeriod,
                        'policyPaths': _policyPaths
                    }}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT policyName, policyVersion, policyDescription, policyComment, policyIdentifier, policyPeriod FROM policy ORDER BY policyName DESC')
            data = cursor.fetchall()

            policy_list = []
            for policy in data:
                cursor1 = db.execute('SELECT policyPathName FROM linkPolicyPath WHERE policyName=?', (policy[0],))
                data1 = cursor1.fetchall()

                path_list = []
                for path in data1:
                    path_list.append(path[0])

                i = {
                    'policyName': policy[0],
                    'policyVersion': policy[1],
                    'policyDescription': policy[2],
                    'policyComment': policy[3],
                    'policyIdentifier': policy[4],
                    'policyPeriod': policy[5],
                    'policyPath': path_list
                }
                policy_list.append(i)

            return {'Status Code': '200', 'policy': policy_list}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkPolicyPath')
            db.execute('DELETE FROM policy')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singlePolicy(Resource):
    def delete(self, policyName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkPolicyPath WHERE policyName=?', (policyName,))
            db.execute('DELETE FROM policy WHERE policyName=?', (policyName,))
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class router(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('routerName', type=str, help='')
            parser.add_argument('routerAddress', type=str, help='')
            parser.add_argument('routerUsername', type=str, help='')
            parser.add_argument('routerPassword', type=str, help='')
            parser.add_argument('routerPort', type=int, help='')

            args = parser.parse_args()

            _routerName = args['routerName']
            _routerAddress = args['routerAddress']
            _routerUsername = args['routerUsername']
            _routerPassword = args['routerPassword']
            _routerPort = args['routerPort']

            db = get_db()
            cursor = db.execute(
                'INSERT INTO router (routerName, routerAddress, routerUsername, routerPassword, routerPort) VALUES (?, ?, ?, ?, ?)',
                [_routerName, _routerAddress, _routerUsername, _routerPassword, _routerPort])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {
                    'router': {
                        'routerName': _routerName,
                        'routerAddress': _routerAddress,
                        'routerUsername': _routerUsername,
                        'routerPassword': _routerPassword,
                        'routerPort': _routerPort
                    }}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT routerName, routerAddress, routerUsername, routerPassword, routerPort FROM router ORDER BY routerName DESC')
            data = cursor.fetchall()

            router_list = []
            for router in data:
                i = {
                    'routerName': router[0],
                    'routerAddress': router[1],
                    'routerUsername': router[2],
                    'routerPassword': router[3],
                    'routerPort': router[4]
                }
                router_list.append(i)

            return {'Status Code': '200', 'router': router_list}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM router')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singleRouter(Resource):
    def delete(self, routerName):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM router WHERE routerName=?', (routerName,))
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class subscriptionRouterLink(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('subscriptionName', type=str, help='')
            parser.add_argument('routers', action='append')
            parser.add_argument('status', type=bool, help='')

            args = parser.parse_args()

            _subscriptionName = args['subscriptionName']
            _routers = args['routers']
            _status = args['status']

            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')

            _linkId = db.execute('SELECT ifnull(max(linkId), 0) + 1 from linkSubscriptionRouter').fetchone()[0]

            router_list = []

            for router in _routers:
                cursor = db.execute(
                    'INSERT INTO linkSubscriptionRouter (linkId, subscriptionName, routerName, status) VALUES (?, ?, ?, ?)',
                        [_linkId, _subscriptionName, router, _status])
                data = cursor.fetchall()

                if len(data) is 0:
                    db.commit()

                    router_list.append(router)

        except Exception as e:
            return {'error': str(e)}

        if len(router_list) > 0:

            return {
                'subscriptionRouterLink': {
                    'linkId': _linkId,
                    'subscriptionName': _subscriptionName,
                    'routers': router_list,
                    'status': _status
            }}

        else:
            return {'Status Code': '1000', 'Message': str(data[0])}


    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT linkId, subscriptionName, status from linkSubscriptionRouter ORDER BY linkId')
            data = cursor.fetchall()

            subscription_router_list = []

            link_id = 0

            for subscription in data:
                if link_id != subscription[0]:
                    link_id = subscription[0]
                    cursor1 = db.execute(
                        'SELECT routerName from linkSubscriptionRouter WHERE linkId=?', (subscription[0],)
                    )
                    data1 = cursor1.fetchall()

                    router_list = []
                    for router in data1:
                        router_list.append(router[0])

                    i = {
                        'linkId': subscription[0],
                        'subscriptionName': subscription[1],
                        'status': subscription[2],
                        'routers': router_list
                    }

                    subscription_router_list.append(i)

            return {'Status Code': '200', 'subscriptionRouterLink': subscription_router_list}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkSubscriptionRouter')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singleSubscriptionRouterLink(Resource):
    def delete(self, linkId):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkSubscriptionRouter WHERE linkId=?', (linkId,))
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}


class policyRouterLink(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('policyGroupName', type=str, help='')
            parser.add_argument('routers', action='append')
            parser.add_argument('status', type=bool, help='')

            args = parser.parse_args()

            _policyGroupName = args['policyGroupName']
            _routers = args['routers']
            _status = args['status']

            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')

            _linkId = db.execute('SELECT ifnull(max(linkId), 0) + 1 from linkPolicyRouter').fetchone()[0]

            router_list = []

            for router in _routers:
                cursor = db.execute(
                    'INSERT INTO linkPolicyRouter (linkId, policyGroupName, routerName, status) VALUES (?, ?, ?, ?)',
                        [_linkId, _policyGroupName, router, _status])
                data = cursor.fetchall()

                if len(data) is 0:
                    db.commit()

                    router_list.append(router)

        except Exception as e:
            return {'error': str(e)}

        if len(router_list) > 0:

            return {
                'policyRouterLink': {
                    'linkId': _linkId,
                    'policyGroupName': _policyGroupName,
                    'routers': router_list,
                    'status': _status
            }}

        else:
            return {'Status Code': '1000', 'Message': str(data[0])}


    def get(self):
        try:
            db = get_db()
            cursor = db.execute(
                'SELECT linkId, policyGroupName, status from linkPolicyRouter ORDER BY linkId')
            data = cursor.fetchall()

            policy_router_list = []

            link_id = 0

            for policy in data:
                if link_id != policy[0]:
                    link_id = policy[0]
                    cursor1 = db.execute(
                        'SELECT routerName from linkPolicyRouter WHERE linkId=?', (policy[0],)
                    )
                    data1 = cursor1.fetchall()

                    router_list = []
                    for router in data1:
                        router_list.append(router[0])

                    i = {
                        'linkId': policy[0],
                        'policyGroupName': policy[1],
                        'status': policy[2],
                        'routers': router_list
                    }

                    policy_router_list.append(i)

            return {'Status Code': '200', 'policyRouterLink': policy_router_list}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkPolicyRouter')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}

class singlePolicyRouterLink(Resource):
    def delete(self, linkId):
        try:
            db = get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM linkPolicyRouter WHERE linkId=?', (linkId,))
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(subscription, '/subscription')
api.add_resource(destinationGroup, '/destinationGroup')
api.add_resource(sensor, '/sensor')
api.add_resource(policyGroup, '/policyGroup')
api.add_resource(collector, '/collector')
api.add_resource(policy, '/policy')
api.add_resource(router, '/router')
api.add_resource(subscriptionRouterLink, '/subscriptionRouterLink')
api.add_resource(policyRouterLink, '/policyRouterLink')
api.add_resource(singleSubscriptionRouterLink, '/subscriptionRouterLink/<linkId>')
api.add_resource(singlePolicyRouterLink, '/policyRouterLink/<linkId>')
api.add_resource(singleRouter, '/router/<routerName>')
api.add_resource(singleSubscription, '/subscription/<subscriptionName>')
api.add_resource(singleDestinationGroup, '/destinationGroup/<destinationGroupName>')
api.add_resource(singleSensor, '/sensor/<sensorName>')
api.add_resource(singlePolicyGroup, '/policyGroup/<policyGroupName>')
api.add_resource(singleCollector, '/collector/<collectorName>')
api.add_resource(singlePolicy, '/policy/<policyName>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True, threaded=True)
