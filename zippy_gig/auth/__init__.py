from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin

from zippy_gig.auth.signup import SignUpController
from zippy_gig.auth.get_token import GetTokenController
from zippy_gig.auth.verify_token import VerifyTokenController
from zippy_gig.decorators import jsonify_result, crossdomain
from zippy_gig import basic_auth
from zippy_gig.models import Account

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/signup/", methods=['POST'])
@jsonify_result
def signup():
    return SignUpController(request)()


# @auth.route("/signin/", methods=['POST'])
# @jsonify_result
# def signin():
#     return SignInController(request)()


@auth.route('/token/', methods=["POST"])
@jsonify_result
@cross_origin(origin="http://localhost:8000")
def get_auth_token():
    return GetTokenController(request)()


@basic_auth.verify_token
def verify_token(token):
    return VerifyTokenController(token)()


