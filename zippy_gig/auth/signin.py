from hashlib import sha1

from flask import session

from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Account


class SignInController(BaseController):
    def __init__(self, request, account=None):
        super(SignInController, self).__init__(request, account)

    def _call(self):
        account = self._check_email()
        self._check_password(account)
        self.account = account
        self._log_in_account()
        return account.get_data()

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

    def _log_in_account(self):
        session.clear()
        session["u"] = self.account.email


