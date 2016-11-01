from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin

from zippy_gig.auth.signup import SignUpController
from zippy_gig.auth.get_token import GetTokenController
from zippy_gig.auth.verify_token import VerifyTokenController
from zippy_gig.decorators import jsonify_result, validate_json
from zippy_gig.auth.edit_prof import EditProfileController
from zippy_gig import token_auth

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.route("/signup/", methods=['POST'])
@validate_json
@cross_origin(headers=['Content-type'])
@jsonify_result
def signup():
    return SignUpController(request)()


@auth.route('/token/', methods=["POST", "OPTIONS"])
# @validate_json
@cross_origin(headers=['Content-type'])
@jsonify_result
def get_auth_token():
    return GetTokenController(request)()


@auth.route("/profile/", methods=['POST'])
@token_auth.login_required
@cross_origin(headers=['Content-Type', 'Authorization'])
@validate_json
@jsonify_result
def mod_profile():
    return EditProfileController(request)()


@token_auth.verify_password
def verify_password(username_or_token, password=None):
    return VerifyTokenController(username_or_token)()
