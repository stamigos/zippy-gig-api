from flask import Blueprint, request, jsonify

from zippy_gig.client.get_vendors import GetVendorsController
from zippy_gig.client.get_profile import GetProfileController
from zippy_gig.decorators import jsonify_result, login_required
from zippy_gig import basic_auth


client = Blueprint('client', __name__, url_prefix='/client')


@client.route("/vendors/", methods=['GET'])
@jsonify_result
def get_vendors():
    return GetVendorsController(request)()


@client.route("/profile/", methods=['GET'])
@basic_auth.login_required
def get_profile():
    return jsonify(GetProfileController(request)())
