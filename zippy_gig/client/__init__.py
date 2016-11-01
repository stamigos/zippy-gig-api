from flask import Blueprint, request, jsonify, g, send_file
from flask_cors import cross_origin

from zippy_gig.client.get_vendors import GetVendorsController
from zippy_gig.client.get_profile import GetProfileController
from zippy_gig.client.get_job_types import GetJobTypesController
from zippy_gig.decorators import jsonify_result
from zippy_gig import token_auth
from zippy_gig.models import Account
from config import MEDIA_ROOT


client = Blueprint('client', __name__, url_prefix='/api/v1/client')


@client.route("/vendors/", methods=['GET'])
@cross_origin(headers=['Content-Type'])
@token_auth.login_required
# @jsonify_result
def get_vendors():
    return jsonify(GetVendorsController(request)())


@client.route("/job-types/", methods=['GET'])
@cross_origin(headers=['Content-Type'])
@token_auth.login_required
# @jsonify_result
def get_job_types():
    return jsonify(GetJobTypesController(request)())


@client.route("/profile/", methods=['GET'])
@token_auth.login_required
@cross_origin(headers=['Content-Type', 'Authorization'])
@jsonify_result
def get_profile():
    return GetProfileController(request)()


@client.route("/avatar/", methods=['POST'])
@token_auth.login_required
@cross_origin(headers=['Content-Type', 'Authorization'])
def file_upload():
    url = g.account.upload_photo()
    return jsonify(dict(result=True, data={"url": url}, error=None))


@client.route('/media/<name>', methods=['GET'])
def img(name):
    return send_file(MEDIA_ROOT + '/' + name, mimetype="image/jpg")
