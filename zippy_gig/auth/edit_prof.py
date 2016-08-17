from hashlib import sha1

from flask import g
from zippy_gig.base import BaseController, ApiException
import phonenumbers
from zippy_gig.constants import AccountType


class EditProfileController(BaseController):

    def __init__(self, request):
        super(EditProfileController, self).__init__(request)

    def _call(self):
        g.account.first_name = self._verify_field('first_name')
        g.account.last_name = self._verify_field('last_name')
        g.account.address = self._verify_field('address')
        g.account.phone = self.check_phone(self._verify_field('phone'))
        g.account.alt_phone = self.check_phone(self._verify_field('alt_phone'))
        g.account.pay_pal = self._verify_field('pay_pal')
        g.account.type = self.check_type(self._verify_field('type'))
        g.account.zip_code = self._verify_field('zip_code')
        g.account.save()

        return g.account.get_profile()

    def check_phone(self, phone):
        try:
            parsed_phone_number = phonenumbers.parse(phone)
        except ApiException, ex:
            raise ApiException('Invalid phone number: %s %s' %
                               (phone, ex.message))

        if not phonenumbers.is_valid_number(parsed_phone_number):
            raise ApiException('Invalid phone number: %s' % (phone))

        return phone

    def check_type(self, _type):
        if _type in [str(e.value) for e in AccountType]:
            return _type
        raise ApiException("Invalid type: %s" % (_type))
