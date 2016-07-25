from zippy_gig.base import BaseController
from zippy_gig.models import Account


class GetVendorsController(BaseController):
    def __init__(self, request):
        super(GetVendorsController, self).__init__(request)

    def _call(self):
        return [account.get_data() for account in Account.get_vendors()]
