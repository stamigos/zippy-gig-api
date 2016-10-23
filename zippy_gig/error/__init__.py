from flask import make_response, jsonify
from flask import Blueprint


error = Blueprint('error', __name__, url_prefix='/error')


@error.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify(dict(result=False, data=None, error="Not found")), 404)


@error.app_errorhandler(401)
def unauthorized():
    return make_response(jsonify(dict(result=False, data=None, error="Unauthorized access")), 401)
