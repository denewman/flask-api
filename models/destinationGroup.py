from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_restful.utils import cors
import sqlite3
import os

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
            cursor = db.execute('INSERT INTO destinationGroup (destinationGroupName, destinationGroupAddress, destinationGroupPort, destinationGroupEncoding, destinationGroupProtocol) values (?, ?, ?, ?)',
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
