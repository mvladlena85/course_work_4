from project.dao.main import UsersDAO
from project.exceptions import ItemNotFound
from project.tools.security import compose_passwords, generate_password_hash


class UsersService:

    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def get_by_id(self, pk):
        if user := self.dao.get_by_id(pk):
            return user
        else:
            raise ItemNotFound(f'User with pk={pk} not exists.')

    def update(self, email, user_d):
        user = self.dao.get_by_email(email)

        if 'name' in user_d:
            user.name = user_d["name"]
        if 'surname' in user_d:
            user.surname = user_d['surname']
        if 'favorite_genre' in user_d:
            user.favorite_genre = user_d['favorite_genre']

        self.dao.update(user)
        return self.dao

    def update_password(self, email, old_password, new_password):
        user = self.dao.get_by_email(email)
        password_hash = user.password

        if compose_passwords(password_hash=password_hash, password=old_password):
            new_password_hash = generate_password_hash(new_password)
            user.password = new_password_hash
            self.dao.update(user)
            return self.dao
        else:
            return None
