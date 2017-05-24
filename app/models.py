"""Models and database functions for Kid-O project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
import os
from uuid import uuid4
from datetime import datetime

from . import app

# This is the connection to the postgres database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


class UUID(PGUUID):
    """Custom UUID type to set some defaults on the Postgres UUID type"""

    def __init__(self, *args, **kwargs):
        if 'as_uuid' not in kwargs:
            kwargs['as_uuid'] = True
        super(UUID, self).__init__(*args, **kwargs)
        self.__module__ = 'sa.dialects.postgresql'


class User(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = bcrypt.generate_password_hash(kwargs['password'])
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User id=%s first_name=%s last_name=%s email=%s password=%s>" % (self.id, self.first_name, self.last_name, self.email, self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """ Returns True if the password is correct for the user.
        """
        return bcrypt.check_password_hash(unicode(self.password), unicode(password.decode("utf8")))
    

class Child(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    photo_url = db.Column(db.String(3000))
    is_active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    nick_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    nationality = db.Column(db.String(200))
    guardian_type = db.Column(db.String(50), nullable=True)
    guardian_fname = db.Column(db.String(32), nullable=True)
    guardian_lname = db.Column(db.String(32), nullable=True)
    number_of_siblings = db.Column(db.Integer)
    siblings_in_project = db.Column(db.String)
    school_class = db.Column(db.String(50))
    school_attendance = db.Column(db.String(50))
    volunteer_task = db.Column(db.String)
    situation = db.Column(db.String)
    godparent_status = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    godparents = db.relationship('Godparent', secondary='child_to_godparent', backref='child', lazy='dynamic', collection_class=set)
    messages = db.relationship('Message', backref='child', lazy='dynamic')

    def __repr__(self):
        return "<Child id=%s first_name=%s last_name=%s>" % (self.id, self.first_name, self.last_name)

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name

    @property
    def age(self):
        currenttime = datetime.now()
        age = currenttime - self.birth_date
        age = age.days / 365
        return age

    def to_dict(self):
        return dict(
            id = self.id,
            pic_url = self.pic_url,
            is_active = self.is_active,
            first_name = self.first_name,
            last_name = self.last_name,
            nick_name = self.nick_name,
            birth_date = self.birth_date,
            nationality = self.nationality,
            guardian_fname = self.guardian_fname,
            guardian_lname = self.guardian_lname,
            guardian_type = self.guardian_type,
            number_of_siblings = self.number_of_siblings,
            siblings_in_project = self.siblings_in_project,
            school_class = self.school_class,
            school_attendance = self.school_attendance,
            volunteer_task = self.volunteer_task,
            situation = self.situation,
            godparent_status = self.godparent_status,
            latitude = self.latitude,
            longitude = self.longitude,
        )


class ChildToGodparent(db.Model):
    child_id = db.Column(UUID(), db.ForeignKey('child.id'), primary_key=True)
    godparent_id = db.Column(UUID(), db.ForeignKey('godparent.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class Godparent(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    messages = db.relationship('Message', backref='godparent', lazy='dynamic')


class Message(db.Model):
    """Message to godparent from Kid-O App."""

    id = db.Column(UUID(), primary_key=True, default=uuid4)
    godparent_id = db.Column(UUID(), db.ForeignKey("godparent.id"), nullable=False)
    child_id = db.Column(UUID(), db.ForeignKey("child.id"), nullable=False)
    subject = db.Column(db.String())
    text_content = db.Column(db.String(8000), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime())
    sent_ok = db.Column(db.Boolean())
    error = db.Column(db.String())
