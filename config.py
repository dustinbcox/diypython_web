"""diypython website"""

import os

def get_config(name, default = ""):
    """Try to read the config from env then filesystem"""

    value = os.getenv(name, default)
    if not value:
        try:
            with open(os.path.join("/etc/secret/", name.lower()), "r") as fh:
                    value = fh.read()
        except FileNotFoundError:
            pass
    return value

# Configuration for the Flask-Bcrypt extension
BCRYPT_LEVEL = int(get_config("BCRYPT_LEVEL", "12"))

SECRET_KEY = get_config("SECRET_KEY").encode()

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = get_config("DATABASE_URI")
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True # overhead
