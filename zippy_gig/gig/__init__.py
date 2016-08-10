from flask import Blueprint, request
from zippy_gig.gig.create_new_work import CreateNewWorkController
from zippy_gig.gig.get_work import GetWorkController
from zippy_gig.gig.get_all_works import GetAllWorksController
from zippy_gig.decorators import jsonify_result, validate_json

gig = Blueprint('gig', __name__, url_prefix='/api/v1/gig')

@gig.route("/", methods=['POST', 'GET'])
@validate_json
@jsonify_result
def create_new_work():
    if request.method == 'POST':
        return CreateNewWorkController(request)()
    else:
        return GetAllWorksController(request)()    

@gig.route("/<int:id>/")
@jsonify_result
def get_work(id):
    return GetWorkController(request)(id)
