from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service, genre_service, user_service
from project.tools.security import generate_token, refresh_tokens

api = Namespace('auth')


@api.route('/register')
class RegisterView(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        name = request.json.get('name')
        surname = request.json.get('surname')
        favorite_genre = request.json.get('favorite_genre')

        genre = genre_service.get_by_name(favorite_genre)

        auth_service.register_user(email=email, password=password,
                                   name=name, surname=surname,
                                   favorite_genre=genre.id)
        return "User created", 201


@api.route('/login')
class LoginView(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')

        user = user_service.get_by_email(email)
        password_hash = user.password

        tokens = generate_token(username=email, password=password, password_hash=password_hash, is_refresh=False)
        if tokens is None:
            return "Некорректные имя пользователя или пароль", 401
        return tokens, 201

    def put(self):
        refresh_token = request.json.get("refresh_token")

        tokens = refresh_tokens(refresh_token)
        if tokens is None:
            return "Некорректный токен", 401
        return tokens, 201


