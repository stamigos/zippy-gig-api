from flask import Blueprint, request

from zippy_gig.auth.signup import SignUpController
from zippy_gig.auth.signin import SignInController

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/signup/", methods=['POST'])
def signup():
    return SignUpController(request)()


@auth.route("/signin/", methods=['POST'])
def signin():
    return SignInController(request)()
