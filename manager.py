# coding: utf-8
from user_service import init_app, app
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from user_service.models import *

init_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()