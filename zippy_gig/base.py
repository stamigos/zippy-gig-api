from flask import jsonify
import json


class ApiException(Exception):
    pass


class BaseController(object):
    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kwargs):
        try:
            # self._verify_data()
            data = self._call(*args, **kwargs)
            return dict(result=True, data=data, error=None)
        except ApiException, e:
            return dict(result=False, data=None, error=e.message)

    def _call(self, *args, **kwargs):
        raise NotImplementedError()

    def _verify_field(self, field):
        try:
            self.request.get_json()[field]
        except KeyError:
            raise ApiException("{field} required".format(field=field))
        return self.request.get_json()[field]

    # def _verify_data(self):
    #     if self.request.method == "POST" and (not self.request.get_json()):
    #         raise ApiException("No json data received")







