from flask import request
from flask_restx import Namespace, Resource
from project.setup.api.models import user


from project.container import user_service, genre_service
from project.tools.security import token_check, get_token_data, compose_passwords, generate_password_hash

api = Namespace('user')


@api.route("/")
class UsersView(Resource):
    @token_check
    @api.response(404, 'Not Found')
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        headers = request.headers['Authorization']
        token = headers.split("Bearer ")[-1]
        data = get_token_data(token)
        email = data.get('username')
        return user_service.get_by_email(email)

    @token_check
    @api.response(404, 'Not Found')
    def patch(self):
        headers = request.headers['Authorization']
        token = headers.split("Bearer ")[-1]
        data = get_token_data(token)
        email = data.get('username')
        user_d = request.json
        genre = genre_service.get_by_name(user_d['favorite_genre'])
        user_d['favorite_genre'] = genre.id

        user_service.update(email, user_d)
        return "", 204


@api.route("/password/")
class UserPasView(Resource):
    @token_check
    def put(self):
        headers = request.headers['Authorization']
        token = headers.split("Bearer ")[-1]
        data = get_token_data(token)
        email = data.get('username')
        print(email)

        user_d = request.json
        old_password = user_d.get('old_password')
        new_password = user_d.get('new_password')

        update_password = user_service.update_password(email=email, old_password=old_password, new_password=new_password)
        if update_password is None:
            return "Введен некорректный пароль", 404
        else:
            return "Пароль успешно обновлен", 204




