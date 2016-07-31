from flask import g
from zippy_gig.base import BaseController


class GetProfileController(BaseController):
    def __init__(self, request):
        super(GetProfileController, self).__init__(request)

    def _call(self):
        return g.account.get_profile()
