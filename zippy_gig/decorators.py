from flask import jsonify, session, request, Response
from functools import wraps


def jsonify_result(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        result = func(*args, **kwds)
        return jsonify(result)
    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        print 'in decor: ', session
        if "u" in session:
            account = session["u"]
            return func(account, *args, **kwds)
        return dict(result=False, data=None,
                    error="You need to login before proceed")
    return wrapper


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth.username or not auth.password or not valid_credentials(auth.username, auth.password):
            return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        return f(*args, **kwargs)
    return wrapper
