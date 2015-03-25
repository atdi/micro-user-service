# coding: utf-8

from user_service import db
from .core import BaseModel, generate_uuid
from sqlalchemy.orm import validates
from flask_restless.helpers import to_dict


roles_users = db.Table('roles_users', BaseModel.metadata,
                       db.Column('user_id', db.String(255), db.ForeignKey('users.id')),
                       db.Column('role_id', db.String(255), db.ForeignKey('roles.id')))


class User(BaseModel):
    id = db.Column(db.String(255), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
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
    customer_id = db.Column(db.String(255), db.ForeignKey('customers.id'),nullable=True)
    customer = db.relationship('Customer')
    __tablename__ = 'users'

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    @staticmethod
    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def to_dict(self):
        return to_dict(self, deep={'roles': []})


class Role(BaseModel):
    id = db.Column(db.String(255), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(200))
    __tablename__ = 'roles'

    def to_dict(self):
        return to_dict(self)


class Country(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    regions = db.relationship("Region", backref="country")
    __tablename__ = 'countries'


class Region(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    cities = db.relationship("City", backref="region")
    __tablename__ = 'regions'


class City(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    __tablename__ = 'cities'


class Customer(BaseModel):
    id = db.Column(db.String(255), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(2), nullable=False)
    unique_id = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    iban = db.Column(db.String(50), nullable=True)
    bank = db.Column(db.String(100), nullable=True)
    swift = db.Column(db.String(20), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship(City)
    addresses = db.relationship("Address", backref="customer")
    __tablename__ = 'customers'


class Address(BaseModel):
    id = db.Column(db.String(255), primary_key=True, default=generate_uuid)
    contact_person = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, default=False)
    customer_id = db.Column(db.String(255), db.ForeignKey('customers.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship(City)
    __tablename__ = 'addresses'
