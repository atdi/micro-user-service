# coding: utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')