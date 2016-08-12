from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig


class DeleteWorkController(BaseController):
    def __init__(self, request):
        super(DeleteWorkController, self).__init__(request)

    def _call(self, id):
        try:
            gig = Gig.get(Gig.id == id)            
        except Gig.DoesNotExist:
            raise ApiException('Work with id: %s does not exist' % id)

        gig.delete().where(Gig.id == id).execute()            
        return {"id:": id}
