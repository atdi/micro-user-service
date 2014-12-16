from distutils.core import setup

setup(
    name='micro-user-service',
    version='0.1',
    packages=['user_service'],
    url='',
    license='GPLv3',
    author='aurel.avramescu',
    author_email='aurel.avramescu@gmail.com',
    description='User service',
    requires=['sqlalchemy',
              'flask',
              'flask-sqlalchemy',
              'flask-restless',
              'flask-script',
              'flask-migrate',
              'alembic',
              'pyhamcrest',
              'tornado',
              'mysql-connector-python']
)
