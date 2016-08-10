from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig

class GetWorksController(BaseController):
    def __init__(self, request):
        super(GetWorksController, self).__init__(request)
        
    def _call(self):    
        return [_gig.get_gig() for _gig in Gig.select()]
        