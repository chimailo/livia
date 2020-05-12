from functools import wraps

from flask import request

from app.models import User
from app.errors import error_response


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return error_response(403, message='Invalid token.')

        token = auth_header.split(" ")[1]
        payload = User.decode_auth_token(token)

        if not isinstance(payload, dict):
            return error_response(401, message=payload)
        print(payload)

        user = User.find_by_id(payload.get('id'))

        if not user or not user.is_active:
            return error_response(401, message='Invalid token.')

        return func(payload.get('id'), *args, **kwargs)
    return wrapper


def status_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = User.find_by_id(id)

        if not user or not user.is_admin:
            return error_response(
                401,
                message='You do not have the required status.'
            )

        return func(*args, **kwargs)

    return wrapper
