from zippy_gig.base import BaseController
from zippy_gig.models import Account


class GetVendorsController(BaseController):
    def __init__(self, request, account=None):
        super(GetVendorsController, self).__init__(request, account)

    def _call(self):
        return [account.get_data() for account in Account.get_vendors()]
