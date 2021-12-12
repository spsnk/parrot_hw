from functools import wraps
from flask_restful import request
from flask import jsonify, abort
import jwt
from api.config import Config
from api.models.shared import db
from api.models.user import Users as UsersModel
import datetime
import os


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            abort(401)
        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            if datetime.datetime.fromtimestamp(data["expires"]) < datetime.datetime.now():
                abort(401)
            current_user = db.session.query(UsersModel).filter_by(
                email=data['email']).first()
            if not current_user:
                abort(401)
            authorized_user = current_user.get_dict().get("email").lower()
            requested_user = kwargs.get("id").lower()
            if authorized_user != requested_user:
                abort(401)
        except Exception as e:
            abort(401)
        return f(*args, **kwargs)
    return decorator


def generate_token(email):
    expiration_minutes = int(os.getenv("TOKEN_EXPIRE_MINUTES", 10))
    expiration_seconds = int(os.getenv("TOKEN_EXPIRE_SECONDS", 0))
    token = jwt.encode({
        'email': email,
        'expires': datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes, seconds=expiration_seconds))
    }, Config.SECRET_KEY, algorithm="HS256")
    return token
