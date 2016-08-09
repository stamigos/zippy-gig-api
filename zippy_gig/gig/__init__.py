from flask import Blueprint, request
from zippy_gig.gig.create_new_work import CreateNewWork
from zippy_gig.decorators import jsonify_result, validate_json

gig = Blueprint('gig', __name__, url_prefix='/api/v1/gig')

@gig.route("/", methods=['POST'])
@validate_json
@jsonify_result
def create_new_work():
    return CreateNewWork(request)()

