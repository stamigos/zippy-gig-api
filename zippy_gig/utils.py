import random
from hashlib import sha1


def hash_pswd(password):
    return sha1(password).hexdigest()


def get_random_string(length=64,
                      allowed_chars='0123456789abcdefghijklmnopqvwxyz'):
    return ''.join(random.choice(allowed_chars) for i in range(length))
