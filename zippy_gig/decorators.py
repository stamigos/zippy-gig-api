from datetime import timedelta
from werkzeug.exceptions import BadRequest
from functools import wraps, update_wrapper

from flask import jsonify, session, request, current_app, make_response


def jsonify_result(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        print 'result: ', result
        return jsonify(result)
    return wrapper


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest, e:
            msg = "Invalid json data"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)
    return wrapper

