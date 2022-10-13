from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    """
    Модель SQLAlchemy для объекта "режиссер".
    """
    __tablename__ = 'director'

    name = Column(String(255), unique=True, nullable=False)
    
    
class Movie(models.Base):
    """
    Модель SQLAlchemy для объекта "фильм".
    """
    __tablename__ = 'movie'
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False, )
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("director.id"), nullable=False)
    director = relationship("Director")


class User(models.Base):
    """
    Модель SQLAlchemy для объекта "пользователь".
    """
    __tablename__ = 'user'
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    surname = Column(String)
    favorite_genre = Column(String, ForeignKey("genres.id"))
    genre = relationship("Genre")
