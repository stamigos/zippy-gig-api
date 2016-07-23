from flask import Blueprint, request

from zippy_gig.client.get_vendors import GetVendorsController


client = Blueprint('client', __name__, url_prefix='/client')


@client.route("/vendors/", methods=['GET'])
def get_vendors():
    return GetVendorsController(request)()
