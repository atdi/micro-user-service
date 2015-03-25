# coding: utf-8
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from user_service import db
import uuid
from flask_restless.helpers import to_dict


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def to_dict(self):
        return to_dict(self)


def generate_uuid():
    return str(uuid.uuid4())


class AbstractModel(CRUDMixin):
    version = db.Column(db.DateTime, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(120), nullable=True)


BaseModel = declarative_base(cls=AbstractModel)
BaseModel.query = db.session.query_property()