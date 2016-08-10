from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig

class GetAllWorksController(BaseController):
    def __init__(self, request):
        super(GetAllWorksController, self).__init__(request)
        
    def _call(self):    
        return [g.get_gig() for g in Gig.select()]
        