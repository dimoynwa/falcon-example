import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed

def auth_admin_req(req, res, resource, **params):
    user_id = params.get('jwt')
    if user_id:
