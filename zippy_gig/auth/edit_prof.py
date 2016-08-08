from hashlib import sha1

from flask import g
from zippy_gig.base import BaseController, ApiException
import phonenumbers


class EditProfileController(BaseController):
    def __init__(self, request):
        super(EditProfileController, self).__init__(request)

    def _call(self):
        try:
            g.account.first_name = self.request.json['first_name']
            g.account.last_name = self.request.json['last_name']
            g.account.address = self.request.json['address']
            g.account.phone = self.check_phone(self.request.json['phone'])
            g.account.alt_phone = self.check_phone(self.request.json['alt_phone'])
            g.account.pay_pal = self.request.json['pay_pal']
            g.account.type = self.request.json['type']
            g.account.save()
        except KeyError:
            raise ApiException("Error in JSON")
        else:
            return g.account.get_profile()

    def check_phone(self, phone):
        if phonenumbers.is_possible_number(phonenumbers.parse(phone, None)):
            return phone
        raise ApiException("Error in phone")

    def check_type(self, _type):
        if _type in ['1', '2', '3']:
            return _type
        raise ApiException("Error in type")
    
