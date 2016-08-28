from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
import sqlite3
import os

class subscription(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('subscriptionName', type=str, help='Subscription name to create subscription')
            parser.add_argument('destinationGroupName', type=str, help='Destination group to create subscription')
            parser.add_argument('sensorName', type=str, help='Sensor Name to create subscription')
            parser.add_argument('subscriptionInterval', type=double, help='Interval for the new subscription')
            args = parser.parse_args()

            _subscriptionName = args['subscriptionName']
            _destinationGroupName = args['destinationGroupName']
            _sensorName = args['sensorName']
            _subscriptionInterval = args['subscriptionInterval']

            db = get_db()
            cursor = db.execute('INSERT INTO subscription (subscriptionName, destinationGroupName, sensorName, subscriptionInterval) values (?, ?, ?)',
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
    
    #~ def put(self):
		#~ try:
			#~ db = get_db()
			#~ cursor = db.execute('')
			#~ data = cursor.fetchall()
		#~ except Exception as e:
			#~ return {'error': str(e)}
			
	#~ def delete(self):
				#~ try:
			#~ db = get_db()
			#~ cursor = db.execute('')
			#~ data = cursor.fetchall()
		#~ except Exception as e:
			#~ return {'error': str(e)}
