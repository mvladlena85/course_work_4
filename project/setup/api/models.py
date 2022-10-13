from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})


director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
})


movie: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
    'description': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
    'trailer': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
    'year': fields.Integer(required=True),
    'rating': fields.Float(required=True),
    'genre': fields.Nested(genre, required=True),
    'director': fields.Nested(director, required=True)
})
