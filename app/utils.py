from passlib.context import CryptContext

# set default hashing algorithm
pw_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    return pw_context.hash(password)


def verify(plain_pw, hashed_pw):
    return pw_context.verify(plain_pw, hashed_pw)