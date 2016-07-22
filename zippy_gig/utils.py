from hashlib import sha1


def hash_pswd(password):
    return sha1(password).hexdigest()
