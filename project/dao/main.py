from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

    def get_by_name(self, name):
        return self._db_session.query(self.__model__).filter(self.__model__.name == name).first()


class DirectorsDAO(BaseDAO[Genre]):
    __model__ = Director


class MoviesDAO(BaseDAO[Genre]):
    __model__ = Movie

    def get_all_order_by(self, page: Optional[int] = None, filter=None):
        stmt: Query = self._db_session.query(self.__model__)
        if filter == 'new':
            stmt: Query = self._db_session.query(self.__model__).order_by(desc(self.__model__.year))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[Genre]):
    __model__ = User

    def register_user(self, user):
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def get_by_email(self, email):
        try:
            return self._db_session.query(self.__model__).filter(self.__model__.email == email).all()[0]
        except Exception as e:
            print(e)
            return None
