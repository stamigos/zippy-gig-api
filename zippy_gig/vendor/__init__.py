from flask import Blueprint, request
from zippy_gig.vendor.set_vendor_status import SetVendorStatusController
from zippy_gig.vendor.get_vendor_status import GetVendorStatusController
from zippy_gig.vendor.set_vendor_description import SetVendorDescriptionController
from zippy_gig.vendor.get_vendor_description import GetVendorDescriptionController
from zippy_gig.decorators import jsonify_result, validate_json
from zippy_gig import basic_auth

vendor = Blueprint('vendor', __name__, url_prefix='/api/v1/vendor')

@vendor.route("/status/", methods=["POST"])
@basic_auth.login_required
@validate_json
@jsonify_result
def set_vendor_status():
    return SetVendorStatusController(request)()

@vendor.route("/status/", methods=["GET"])
@basic_auth.login_required
@validate_json
@jsonify_result
def get_vendor_status():
    return GetVendorStatusController(request)()

@vendor.route("/description/", methods=["POST"])
@basic_auth.login_required
@validate_json
@jsonify_result
def set_vendor_description():
    return SetVendorDescriptionController(request)()

@vendor.route("/description/", methods=["GET"])
@basic_auth.login_required
@validate_json
@jsonify_result
def get_vendor_description():
    return GetVendorDescriptionController(request)()
