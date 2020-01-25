from app import app
from flask_restful import Resource, Api
from bson.json_util import dumps
from app import db

api = Api(app)

class FindUser(Resource):
    def get(self):
        try:
            users = db.find()
        except Exception as e:
            return {'Not found': f'{e}'}, 404
        
        return {'data': dumps(users)}, 200


api.add_resource(FindUser, '/api/users')