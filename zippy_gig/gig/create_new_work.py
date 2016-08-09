from zippy_gig.base import BaseController
from zippy_gig.models import Gig

class CreateNewWork(BaseController):
    def __init__(self, request):
        super(CreateNewWork, self).__init__(request)
        
    def _call(self):
        work = Gig(_type=self._verify_field('type'),
                description=self._verify_field('description'),
                price=self._verify_field('price'),
                account=self._verify_field('account'))
                
        work.save()
        return work.__repr__()
