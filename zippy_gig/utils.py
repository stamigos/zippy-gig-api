import random
from hashlib import sha1
import decimal
import flask.json


def hash_pswd(password):
    return sha1(password).hexdigest()


def get_random_string(length=64,
                      allowed_chars='0123456789abcdefghijklmnopqvwxyz'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

class JSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(JSONEncoder, self).default(obj)
