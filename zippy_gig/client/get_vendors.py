from zippy_gig.base import BaseController
from zippy_gig.models import Account
from flask import request


class GetVendorsController(BaseController):
    def __init__(self, request):
        super(GetVendorsController, self).__init__(request)

    def _call(self):
        job_type = request.args.get('job_type')
        status =  request.args.get('status')
    
        return [account.get_data() for account in Account.get_vendors(job_type=job_type ,status=status)]
        