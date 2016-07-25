from hashlib import sha1

from flask import g, request

from zippy_gig.models import Account


class VerifyPasswordController(object):
    def __init__(self, email_or_token, password):
        self.email_or_token = email_or_token
        self.password = password

    def __call__(self):
        account = Account.verify_auth_token(self.email_or_token)
        if not account:
            try:
                account = Account.get(Account.email == self.email_or_token)
            except Account.DoesNotExist:
                return False
            if not account or account.password != sha1(self.password).hexdigest():
                return False
        g.account = account
        return True


