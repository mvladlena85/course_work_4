from project.dao.base import BaseDAO


class UsersService:

    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_by_email(self, email):
        return self.dao.get_by_email(email)
