# coding: utf-8
from user_service import app, init_app
import threading
from sqlalchemy import create_engine
from user_service.core import BaseModel
from user_service.tests.integration.config import basedir
import os
# Tornado imports
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def create_database(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    BaseModel.metadata.create_all(bind=engine)


def shutdown_server():
    IOLoop.instance().stop()


def before_all(context):
    init_app(settings='user_service.tests.integration.config')
    create_database(app)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    ioloop = IOLoop.instance()
    context.server = http_server
    context.thread = threading.Thread(target=ioloop.start)
    context.thread.start()


def after_all(context):
    shutdown_server()
    os.remove(os.path.join(basedir, 'users.db'))