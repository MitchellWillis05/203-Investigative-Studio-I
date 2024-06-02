from werkzeug.security import generate_password_hash, check_password_hash


def encrypt_password(password):
    password_hash = generate_password_hash(password)
    return password_hash


def verify_password(password, pwhash):
    return check_password_hash(pwhash, password)
