import base64
import calendar
import hashlib
import hmac
import datetime
from typing import Union

import jwt
from flask import current_app, request
from flask_restx import abort


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


# TODO: [security] Описать функцию compose_passwords(password_hash: Union[str, bytes], password: str)
def compose_passwords(password_hash: Union[str, bytes], password: str):
    """Валидация пароля по его хешу"""
    return hmac.compare_digest(generate_password_hash(password), password_hash)


def generate_token(username, password, password_hash, is_refresh=True):
    """Генерация пары токенов: "access_token" и "refresh_token" """
    if username is None:
        return None

    if not is_refresh:
        if not compose_passwords(password_hash=password_hash, password=password):
            return None

    data = {"username": username,
            "password": password}

    minutes = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
    data['exp'] = calendar.timegm(minutes.timetuple())
    access_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGO"])

    days = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config["TOKEN_EXPIRE_DAYS"])
    data['exp'] = calendar.timegm(days.timetuple())
    refresh_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGO"])

    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_tokens(token):
    """Обновление пары токенов: "access_token" и "refresh_token" по refresh_token"""
    if token is None:
        return None

    try:
        token_data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])
    except Exception as e:
        return None

    username = token_data.get("username")
    password = token_data.get("password")

    return generate_token(username, password, None, True)


def get_token_data(token):
    try:
        token_data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])
        return token_data
    except Exception as e:
        print(e)
        return None


def token_check(func):
    """Декоратор для проверки, авторизован ли пользователь"""
    def wrapper(*args, **kwargs):
        if 'Authorization'not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGO"]])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, ** kwargs)
    return wrapper


