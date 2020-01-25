from app import app
from flask_restful import Resource, Api
from app import db
from flask import jsonify

api = Api(app)

class FindUsers(Resource):
    def get(self):
        try:
            users = db.find()
        except Exception as e:
            return {'Not found': f'{e}'}, 404
    
        for user in users:
            user['_id'] = str(user['_id'])
        
        response = jsonify(users)
        response.status_code = 200

        return response


class FindUser(Resource):
    def get(self, user_id):
        try:
            user = db.find_by_id(user_id)
        except Exception as e:
            return {'Not found': f'{e}'}, 404
    
        
        user['_id'] = str(user['_id'])
        
        response = jsonify(user)
        response.status_code = 200

        return response

api.add_resource(FindUsers, '/api/users/')
api.add_resource(FindUser, '/api/user/<string:user_id>')