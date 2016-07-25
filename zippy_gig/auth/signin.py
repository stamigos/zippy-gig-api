from hashlib import sha1

from flask import session, g

from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Account


class SignInController(BaseController):
    def __init__(self, request):
        super(SignInController, self).__init__(request)

    def _call(self):
        account = self._check_email()
        self._check_password(account)
        g.account = account
        return account.email

    def _check_email(self):
        email = self._verify_field("email")
        try:
            account = Account.get(Account.email == email)
            return account
        except Account.DoesNotExist:
            raise ApiException("Account {email} does not exists".format(email))

    def _check_password(self, account):
        password = self._verify_field("password")
        if account.password != sha1(password).hexdigest():
            raise ApiException("Password is incorrect")





