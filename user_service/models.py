# coding: utf-8

from user_service import db
from .core import BaseModel
from sqlalchemy.orm import validates
from flask.ext.restless.helpers import to_dict


roles_users = db.Table('roles_users', BaseModel.metadata,
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class User(BaseModel):
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    last_login_at = db.Column(db.DateTime, nullable=True)
    current_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(16), nullable=True)
    current_login_ip = db.Column(db.String(16), nullable=True)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, nullable=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    __tablename__ = 'users'

    def to_dict(self):
        return to_dict(self)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    @staticmethod
    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def __unicode__(self):
        return '%s' % self.email


class Role(BaseModel):
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(200))
    __tablename__ = 'roles'

    def __unicode__(self):
        return '%s' % self.name