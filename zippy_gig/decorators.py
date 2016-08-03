from datetime import timedelta
from functools import wraps, update_wrapper

from flask import jsonify, session, request, current_app, make_response


def jsonify_result(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        return jsonify(result)
    return wrapper

