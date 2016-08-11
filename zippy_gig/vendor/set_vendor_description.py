from hashlib import sha1

from flask import g
from zippy_gig.base import BaseController, ApiException


class SetVendorDescriptionController(BaseController):
    def __init__(self, request):
        super(SetVendorDescriptionController, self).__init__(request)

    def _call(self):       
        g.account.vendor_description = self._verify_field('vendor_description')
        g.account.save()
    
        return {"vendor_description": g.account.vendor_description}        
