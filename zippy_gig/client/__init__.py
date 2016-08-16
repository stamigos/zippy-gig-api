from flask import Blueprint, request, jsonify, g, send_file
from flask_cors import cross_origin

from zippy_gig.client.get_vendors import GetVendorsController
from zippy_gig.client.get_profile import GetProfileController
from zippy_gig.client.get_job_types import GetJobTypesController
from zippy_gig.decorators import jsonify_result
from zippy_gig import basic_auth
from zippy_gig.models import Account
from config import MEDIA_ROOT


client = Blueprint('client', __name__, url_prefix='/api/v1/client')


@client.route("/vendors/", methods=['GET'])
@cross_origin(headers=['Content-Type'])
@jsonify_result
@basic_auth.login_required
def get_vendors():
    return GetVendorsController(request)()


@client.route("/job-types/", methods=['GET'])
@cross_origin(headers=['Content-Type'])
@jsonify_result
def get_job_types():
    return GetJobTypesController(request)()


@client.route("/profile/", methods=['GET'])
@basic_auth.login_required
@cross_origin(headers=['Content-Type', 'Authorization'])
@jsonify_result
def get_profile():
    return GetProfileController(request)()


@client.route("/fileUpload", methods=['POST'])
@basic_auth.login_required
def file_upload():
    acc = Account.get(id=1)
    acc.upload_photo()
    return jsonify(dict(result=True, data={"url": acc.avatar.url()}, error=None))


@client.route('/media/<name>', methods=['GET'])
def img(name):
    return send_file(MEDIA_ROOT + '/' + name, mimetype="image/jpg")
