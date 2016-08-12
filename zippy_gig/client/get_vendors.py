from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Account


class GetVendorsController(BaseController):
    def __init__(self, request):
        super(GetVendorsController, self).__init__(request)

    def _call(self):
        job_type = self._verify_param('job_type')
        vendor_status = self._verify_param('status')
    
        return [account.get_data() for account in Account.get_vendors(job_type=job_type, vendor_status=vendor_status)]

    def _verify_param(self, name):
        if not self.request.args.get(name):
            return None
        return self.request.args.get(name)
