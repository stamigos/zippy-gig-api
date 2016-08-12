from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig


class DeleteWorkController(BaseController):
    def __init__(self, request):
        super(DeleteWorkController, self).__init__(request)

    def _call(self, id):
        try:
            Gig.get(Gig.id == id).get_gig()
        except Gig.DoesNotExist:
            raise ApiException('Work with id: %s does not exist' % id)

        query = Gig.delete().where(Gig.id == id)
        query.execute()
        return {"id:": id}
