from flask import Blueprint, request, jsonify, g

from zippy_gig.auth.signup import SignUpController
from zippy_gig.auth.signin import SignInController
from zippy_gig.auth.verify_password import VerifyPasswordController
from zippy_gig.decorators import jsonify_result
from zippy_gig import basic_auth

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/signup/", methods=['POST'])
@jsonify_result
def signup():
    return SignUpController(request)()


@auth.route("/signin/", methods=['POST'])
@jsonify_result
@basic_auth.verify_password
def signin():
    return SignInController(request)()


@auth.route('/token/')
@basic_auth.login_required
def get_auth_token():
    token = g.account.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@basic_auth.verify_password
def verify_password(email, password):
    return VerifyPasswordController(email, password)()

