"""Models and database functions for Kid-O project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.bcrypt import Bcrypt
import os
from datetime import datetime

from . import app

# This is the connection to the postgres database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


class User(db.Model):
    """User of Kid-O App."""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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
        return bcrypt.check_password_hash(self.password, password)
    

class Child(db.Model):
    """Child of Kid-O App."""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pic_url = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    guardian_type = db.Column(db.String(50), nullable=True)
    guardian_fname = db.Column(db.String(32), nullable=True)
    guardian_lname = db.Column(db.String(32), nullable=True)
    godparent_prefix = db.Column(db.String(32), nullable=True)
    godparent_fname = db.Column(db.String(32), nullable=True)
    godparent_lname = db.Column(db.String(32), nullable=True)
    godparent_email = db.Column(db.String(32), nullable=True)
    medical_condition = db.Column(db.String, nullable=True)
    doctor_appt = db.Column(db.DateTime, nullable=True)
    situation = db.Column(db.Text, nullable=True)
    home_visit = db.Column(db.DateTime, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    activity = db.Column(db.Boolean, nullable=True)
    messages = db.relationship('Message', backref='child', lazy='dynamic')


    def __repr__(self):
        """Provide helpful representation when printed."""

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
            first_name = self.first_name,
            last_name = self.last_name,
            birth_date = self.birth_date,
            guardian_type = self.guardian_type,
            guardian_fname = self.guardian_fname,
            guardian_lname = self.guardian_lname,
            medical_condition = self.medical_condition,
            doctor_appt = self.doctor_appt,
            situation = self.situation,
            home_visit = self.home_visit,
            latitude = self.latitude,
            longitude = self.longitude,
        )

class Godparent(db.Model):
    """A child's godparent."""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    prefix = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    messages = db.relationship('Message', backref='godparent', lazy='dynamic')


class Message(db.Model):
    """Message to godparent from Kid-O App."""

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    godparent_id = db.Column(db.Integer(), db.ForeignKey("godparent.id"), nullable=False)
    child_id = db.Column(db.Integer(), db.ForeignKey("child.id"), nullable=False)
    subject = db.Column(db.String())
    text_content = db.Column(db.String(8000), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime())
    sent_ok = db.Column(db.Boolean())
    error = db.Column(db.String())
