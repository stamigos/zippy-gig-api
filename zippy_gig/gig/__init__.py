from flask import Blueprint, request
from zippy_gig.gig.create_work import CreateWorkController
from zippy_gig.gig.get_work import GetWorkController
from zippy_gig.gig.get_works import GetWorksController
from zippy_gig.decorators import jsonify_result, validate_json

gig = Blueprint('gig', __name__, url_prefix='/api/v1/gig')

@gig.route("/", methods=['POST'])
@validate_json
@jsonify_result
def create_work():
    return CreateWorkController(request)()
    
@gig.route("/<int:id>/")
@jsonify_result
def get_work(id):
    return GetWorkController(request)(id)

@gig.route("/", methods=['GET'])
@validate_json
@jsonify_result
def get_works():
    return GetWorksController(request)()    

