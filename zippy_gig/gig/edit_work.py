from zippy_gig.base import BaseController, ApiException
from zippy_gig.models import Gig


class EditWorkController(BaseController):

    def __init__(self, request):
        super(EditWorkController, self).__init__(request)

    def _call(self, id):
        try:
            gig = Gig.get(Gig.id == id)
        except Gig.DoesNotExist:
            raise ApiException('Work with id: %s does not exist' % id)

        gig._type = self._verify_field('type')
        gig.description = self._verify_field('description')
        gig.price = self._verify_field('price')
        gig.account = self._verify_field('account')

        gig.save()

        return gig.get_gig()
