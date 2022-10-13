from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


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
