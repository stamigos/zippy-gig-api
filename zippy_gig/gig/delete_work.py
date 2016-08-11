from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig


class DeleteWorkController(BaseController):
    def __init__(self, request):
        super(DeleteWorkController, self).__init__(request)

    def _call(self, id):
        print "aaa"
        return {"id": id}
