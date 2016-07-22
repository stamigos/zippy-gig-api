from flask import jsonify


class ApiException(Exception):
    pass


class BaseController(object):
    def __init__(self, request, account=None):
        self.request = request
        self.account = account

    def __call__(self, *args, **kwargs):
        try:
            data = self._call(*args, **kwargs)
            return jsonify(dict(result=True,
                                data=data,
                                error=None))
        except ApiException, e:
            return jsonify(dict(result=False,
                                data=None,
                                error=e.message))

    def _call(self, *args, **kwargs):
        raise NotImplementedError()

    def _verify_field(self, field):
        if not self.request.get_json().get(field):
            raise Exception("{field} required".format(field))
        return self.request.json.get(field)






