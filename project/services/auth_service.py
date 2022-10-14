from project.dao.base import BaseDAO
from project.models import User
from project.tools.security import generate_password_hash


class AuthService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def register_user(self, email, password, name, surname, favorite_genre=None):
        password_hash = generate_password_hash(password)

        user = User(email=email, password=password_hash, name=name, surname=surname, favorite_genre=favorite_genre)
        return self.dao.register_user(user)


