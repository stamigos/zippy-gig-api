from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig

class GetWorkController(BaseController):
    def __init__(self, request):
        super(GetWorkController, self).__init__(request)
        
    def _call(self, id):
        try:
            return Gig.get(Gig.id == id).get_gig()
        except Gig.DoesNotExist:
            raise ApiException('Work with id: %s does not exist' % id)
