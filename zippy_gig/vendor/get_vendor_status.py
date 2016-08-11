from hashlib import sha1

from flask import g
from zippy_gig.base import BaseController, ApiException


class GetVendorStatusController(BaseController):
    def __init__(self, request):
        super(GetVendorStatusController, self).__init__(request)

    def _call(self):
        return {"vendor_status": g.account.vendor_status}
