from bcrypt import gensalt, hashpw, checkpw


def hash_password(password: str):
    return hashpw(password.encode(), gensalt())


def check_password(password: bytes, hashed_passwd: str):
    return checkpw(password, hashed_passwd)
