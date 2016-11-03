from flask_restful import Resource, reqparse
import sqlite_api

class subscription(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('subscriptionId', type=int, help='Subscription ID to create subscription')
            parser.add_argument('subscriptionName', type=str, help='Subscription name to create subscription')
            parser.add_argument('destinationGroupName', type=str, help='Destination group to create subscription')
            parser.add_argument('sensorName', type=str, help='Sensor Name to create subscription')
            parser.add_argument('subscriptionInterval', type=float, help='Interval for the new subscription')
            args = parser.parse_args()

            _subscriptionId = args['subscriptionId']
            _subscriptionName = args['subscriptionName']
            _destinationGroupName = args['destinationGroupName']
            _sensorName = args['sensorName']
            _subscriptionInterval = args['subscriptionInterval']

            db = sqlite_api.get_db()
            db.execute('PRAGMA foreign_keys=ON')
            cursor = db.execute(
                'INSERT INTO subscription (subscriptionId, subscriptionName, destinationGroupName, sensorName, subscriptionInterval) VALUES (?, ?, ?, ?, ?)',
                [_subscriptionId, _subscriptionName, _destinationGroupName, _sensorName, _subscriptionInterval])
            data = cursor.fetchall()

            if len(data) is 0:
                db.commit()
                return {'subscription': {'subscriptionId': _subscriptionId,
                                         'subscriptionName': _subscriptionName,
                                         'destinationGroupName': _destinationGroupName,
                                         'sensorName': _sensorName,
                                         'subscriptionInterval': _subscriptionInterval}}
            else:
                return {'Status Code': '1000', 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

    def get(self):
        try:
            db = sqlite_api.get_db()
            cursor = db.execute(
                'SELECT subscriptionId, subscriptionName, destinationGroupName, sensorName, subscriptionInterval FROM subscription ORDER BY subscriptionName DESC')
            data = cursor.fetchall()

            subscription_list = []
            for subscription in data:
                i = {
                    'subscriptionId': subscription[0],
                    'subscriptionName': subscription[1],
                    'destinationGroupName': subscription[2],
                    'sensorName': subscription[3],
                    'subscriptionInterval': subscription[4]
                }
                subscription_list.append(i)

            return {'Status Code': '200', 'subscription': subscription_list}

        except Exception as e:
            return {'error': str(e)}

    def delete(self):
        try:
            db = sqlite_api.get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM subscription')
            db.commit()
            return {'Status Code': '200'}

        except Exception as e:
            return {'error': str(e)}


class singleSubscription(Resource):
    def get(self, subscriptionName):
        try:
            db = sqlite_api.get_db()
            query = db.execute(
                'SELECT subscriptionId, subscriptionName, destinationGroupName, sensorName, subscriptionInterval FROM subscription WHERE subscriptionName =?',
                (subscriptionName,))
            subscription = query.fetchone()
            data = {
                'subscriptionId': subscription[0],
                'subscriptionName': subscription[1],
                'destinationGroupName': subscription[2],
                'sensorName': subscription[3],
                'subscriptionInterval': subscription[4]
            }

            return {'Status Code': '200', 'data': data}

        except Exception as e:
            return {'error': str(e)}

    def delete(self, subscriptionName):
        try:
            db = sqlite_api.get_db()
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('DELETE FROM subscription WHERE subscriptionName=?', (subscriptionName,))
            db.commit()
            return {'statusCode': '200'}

        except Exception as e:
            return {'error': str(e)}