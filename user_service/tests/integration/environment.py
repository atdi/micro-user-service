# coding: utf-8
from user_service import app, init_app
from flask import request
import threading
import requests
from sqlalchemy import create_engine
from user_service.core import BaseModel
from user_service.tests.integration.config import basedir
import os


def create_database(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    BaseModel.metadata.create_all(bind=engine)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()


def before_all(context):
    init_app(settings='user_service.tests.integration.config')
    create_database(app)
    context.server = app
    context.thread = threading.Thread(target=app.run)
    context.thread.start()


def after_all(context):
    requests.get('http://localhost:5000/shutdown')
    os.remove(os.path.join(basedir, 'users.db'))