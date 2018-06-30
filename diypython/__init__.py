
import platform

USE_POSTGRESQL = True

if USE_POSTGRESQL:
    if platform.python_implementation() == "PyPy":
        print("Detected PyPy loading PostgreSQL Driver")
        from psycopg2cffi import compat
        compat.register()

from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
#app.config.from_pyfile('config.py')

# TODO deprecated
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)

# Define the routes
from . view import *

__all__ = ['app', 'db', 'manager', 'bootstrap']
