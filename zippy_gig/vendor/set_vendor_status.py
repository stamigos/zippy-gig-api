from hashlib import sha1

from flask import g
from zippy_gig.base import BaseController, ApiException


class SetVendorStatusController(BaseController):
    def __init__(self, request):
        super(SetVendorStatusController, self).__init__(request)

    def _call(self):       
        g.account.vendor_status = self._verify_field('vendor_status')
        g.account.save()
    
        return g.account.get_profile()        
