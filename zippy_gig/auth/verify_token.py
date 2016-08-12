from hashlib import sha1

from flask import g, request

from zippy_gig.models import Account


class VerifyTokenController(object):

    def __init__(self, token):
        self.token = token

    def __call__(self):
        account = Account.verify_auth_token(self.token)
        if not account:
            return False
        g.account = account
        return True
