from functools import wraps
from config import auth_token

def require_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        from flask import request

        token = request.args.get('auth_token')

        return func(*args, **kwargs)
    return check_token
