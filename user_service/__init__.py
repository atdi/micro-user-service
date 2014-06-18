# coding: utf-8
from flask import Flask
import flask.ext.restless
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()

rest_manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
from user_service.views import *


def init_app(settings='user_service.config'):
    app.config.from_object(settings)
    db.init_app(app)

