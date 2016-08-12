from hashlib import sha1

from flask import g
from zippy_gig.base import BaseController, ApiException


class GetVendorDescriptionController(BaseController):

    def __init__(self, request):
        super(GetVendorDescriptionController, self).__init__(request)

    def _call(self):
        return {"vendor_description": g.account.vendor_description}
