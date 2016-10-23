from zippy_gig.base import BaseController
from zippy_gig.models import JobType


class GetJobTypesController(BaseController):
    def __init__(self, request):
        super(GetJobTypesController, self).__init__(request)

    def _call(self):
        return {'job_types': [{'id': job_type.id, 'title': job_type.title} for job_type in JobType.select()]}
