from flask import request
from flask_restx import Namespace, Resource

api = Namespace('auth')

@api.route('/register')
class RegisterView(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')


