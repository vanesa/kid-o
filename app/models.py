"""Models and database functions for Kid-O project."""

import hashlib
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import uuid4

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
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(254), nullable=True)
    password = db.Column(db.String(60), nullable=True)  # bcrypt hashes are 60 chars long
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    groups = db.relationship('Group', secondary='user_to_group', lazy='dynamic', collection_class=set)

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            self.set_password(kwargs.pop('password'))
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User id=%s first_name=%s last_name=%s email=%s password=%s>" % (self.id, self.first_name, self.last_name, self.email, self.password)

    @property
    def permissions(self):
        perms = []
        for group in self.groups.all():
            perms.extend([perm.name for perm in group.permissions.all()])
        return list(set(perms))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.password = str(bcrypt.generate_password_hash(password))

    def check_password(self, password):
        """ Returns True if the password is correct for the user."""
        if not self.password or not password:
            return False
        return bcrypt.check_password_hash(self.password, password)


class UserToGroup(db.Model):
    user_id = db.Column(UUID(), db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(UUID(), db.ForeignKey('group.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class Group(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    permissions = db.relationship('Permission', secondary='group_to_permission', backref='group', lazy='dynamic', collection_class=set)
    users = db.relationship('User', secondary='user_to_group', collection_class=set)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    def __repr__(self):
        return '{self.name}'.format(self=self)


class GroupToPermission(db.Model):
    group_id = db.Column(UUID(), db.ForeignKey('group.id'), primary_key=True)
    permission_id = db.Column(UUID(), db.ForeignKey('permission.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class Permission(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    def __repr__(self):
        return '{self.name}'.format(self=self)


class Child(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    photo = db.Column(db.LargeBinary())
    is_active = db.Column(db.Boolean, default=True)
    gender = db.Column(db.String(32))
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    nick_name = db.Column(db.String(32), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    birth_date_accuracy = db.Column(db.String(200))
    nationality = db.Column(db.String(200))
    guardian_type = db.Column(db.String(50))
    guardian_fname = db.Column(db.String(32))
    guardian_lname = db.Column(db.String(32))
    number_of_siblings = db.Column(db.Integer)
    siblings_in_project = db.Column(db.String)
    school_name = db.Column(db.String(150))
    school_class = db.Column(db.String(50))
    school_attendance = db.Column(db.String(50))
    volunteer_task = db.Column(db.String)
    situation = db.Column(db.String)
    godparent_status = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    projects = db.relationship('Project', secondary='child_to_project', backref='child', lazy='dynamic', collection_class=set)
    godparents = db.relationship('Godparent', secondary='child_to_godparent', backref='child', lazy='dynamic', collection_class=set)
    messages = db.relationship('Message', backref='child', lazy='dynamic')

    def __repr__(self):
        return "<Child id=%s first_name=%s last_name=%s photo_url=%s>" % (self.id, self.first_name, self.last_name, self.photo_url)

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name

    @property
    def age(self):
        currenttime = datetime.now()
        age = currenttime - self.birth_date
        age = age.days / 365
        return age

    @property
    def photo_url(self):
        if self.photo is None:
            return '/static/images/childphotopreview.png'
        return '/child_photo/{0}?v={1}'.format(self.id, self.photo_hash)

    @property
    def photo_hash(self):
        return hashlib.md5(self.photo).hexdigest()

    @property
    def projects_for_html(self):
        return [{'name': p.name, 'selected': p in self.projects} for p in Project.query.all()]

    def to_dict(self):
        return dict(
            id = self.id,
            photo_url = self.photo_url,
            is_active = self.is_active,
            first_name = self.first_name,
            last_name = self.last_name,
            nick_name = self.nick_name,
            birth_date = self.birth_date,
            birth_date_accuracy = self.birth_date_accuracy,
            nationality = self.nationality,
            guardian_type = self.guardian_type,
            guardian_fname = self.guardian_fname,
            guardian_lname = self.guardian_lname,
            number_of_siblings = self.number_of_siblings,
            siblings_in_project = self.siblings_in_project,
            school_name = self.school_name,
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
    is_active = db.Column(db.Boolean, default=True)


class Godparent(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    referral_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    messages = db.relationship('Message', backref='godparent', lazy='dynamic')
    sponsorship_history = db.Column(db.String(), nullable=True)
    children = db.relationship('Child', secondary='child_to_godparent', backref='godparent', lazy='dynamic', collection_class=set)
    projects = db.relationship('Project', secondary='godparent_to_project', backref='godparent', lazy='dynamic', collection_class=set)

    def __repr__(self):
        return unicode('{first_name} {last_name}').format(
            first_name=self.first_name,
            last_name=self.last_name,
        )

    @hybrid_property
    def gp_fullname(self):
        return self.first_name + " " + self.last_name


class Project(db.Model):
    id = db.Column(UUID(), primary_key=True, default=uuid4)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return unicode(self.name)


class ChildToProject(db.Model):
    child_id = db.Column(UUID(), db.ForeignKey('child.id'), primary_key=True)
    project_id = db.Column(UUID(), db.ForeignKey('project.id'), primary_key=True)


class GodparentToProject(db.Model):
    godparent_id = db.Column(UUID(), db.ForeignKey('godparent.id'), primary_key=True)
    project_id = db.Column(UUID(), db.ForeignKey('project.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


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
