from . import db

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


class UserRole(db.Model):
    """Define a Role for a User"""
    __tablename__ = 'user_role'
    id      = db.Column(db.Integer,     primary_key = True)
    name    = db.Column(db.String(64),  unique = True, index = True)
    users   = db.relationship('User',   backref='role')

    def __repr__(self):
        return '<UserRole %r>' % self.name

class User(db.Model):
    """A User"""
    __tablename__   = 'user'
    id              = db.Column(db.Integer,     primary_key = True)
    first_name      = db.Column(db.String(50),  nullable = False)
    last_name       = db.Column(db.String(50),  nullable = False)
    role_id         = db.Column(db.Integer,     db.ForeignKey('user_role.id'))    
    username        = db.Column(db.String(128), unique = True, index = True)
    email           = db.Column(db.String(250), unique = True, index = True)
    password        = db.Column(db.String(60))
    gravatar        = db.Column(db.CHAR(32),    nullable = True)
    summary         = db.Column(db.String(250), nullable = True)
    twitter         = db.Column(db.String(150), nullable = True)
    facebook        = db.Column(db.String(150), nullable = True)
    linkedin        = db.Column(db.String(150), nullable = True)
    slack           = db.Column(db.String(50),  nullable = True)

    def __repr__(self):
        return '<User %r>' % self.username

class HttpLog(db.Model):
    """Any HTTP Requests that result in a 404"""
    __tablename__ = 'http_log'
    id          = db.Column(db.Integer, primary_key = True)
    date        = db.Column(db.DateTime(timezone = True), index = True)
    ip          = db.Column(db.CHAR(15))
    referrer    = db.Column(db.String(255))
    verb        = db.Column(db.Enum('HEAD', 'GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'CONNECT', name = 'http_verb'))
    status      = db.Column(db.Integer)
    path        = db.Column(db.Unicode(1024))
    bad         = db.Column(db.Boolean, nullable = True)


class MagicalIpAddress(db.Model):
    """Certain IP addresses have special attributes or properties"""
    id          = db.Column(db.Integer,     primary_key = True)
    ip          = db.Column(db.CHAR(15),    unique = True, index = True)
    name        = db.Column(db.String(25))
    

class Page(db.Model):
    """A given Page"""
    __tablename__ = 'page'
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(120), index = True, unique = True)
    summary     = db.Column(db.String(250))
    date        = db.Column(db.DateTime(timezone = True))
    items       = db.relationship('PageItem', backref = 'page_item')


class PageItem(db.Model):
    """An item on a given Page"""
    __tablename__ = 'page_item'
    id          = db.Column(db.Integer, primary_key = True)
    page        = db.Column(db.Integer, db.ForeignKey('page.id'))
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    date        = db.Column(db.DateTime(timezone = True))
    type        = db.Column(db.Enum('Markdown','Code','Comment','Link','Picture', 'Interactive', name = 'item_type'))
    

def initialize():
    """Create the initial schema + data if needed"""
    from sqlalchemy.engine.reflection import Inspector
    inspector = Inspector.from_engine(db.engine)
    current_tables = set(inspector.get_table_names())
    expected_tables = set(('magical_ip_address', 'http_log', 'user_role', 'page', 'user', 'page_item'))
    if expected_tables.issubset(current_tables):
        print ("Database is already populated")
    else:
        print ("Missing tables - going to create them")
        db.create_all()
        admin_role = UserRole(name='Admin')
        mod_role = UserRole(name='Moderator')
        user_role = UserRole(name='User')
        db.session.add_all([admin_role, mod_role, user_role])
        db.session.commit()

if __name__ == "diypython.model":
    initialize()
