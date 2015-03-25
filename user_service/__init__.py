# coding: utf-8
from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()

rest_manager = APIManager(app, flask_sqlalchemy_db=db)
from user_service.views import *
from user_service.errors import *


def init_app(settings='user_service.config'):
    app.config.from_object(settings)
    db.init_app(app)

