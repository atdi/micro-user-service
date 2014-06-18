# coding: utf-8

import os
import datetime
from sqlalchemy import create_engine
from flask import json
from flask.ext.testing import TestCase
from user_service.core import BaseModel
from user_service.tests.config import basedir
from user_service import init_app, app
from user_service.models import User, Role


def create_database(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    BaseModel.metadata.create_all(bind=engine)


def create_users_and_roles():
    role_customer = Role(name="CUSTOMER").save()
    role_admin = Role(name="ADMIN").save()

    user = User(first_name='First',
                last_name='Last',
                birth_date=datetime.date.today(),
                email='test@email.com',
                password='password').save()

    user.roles.append(role_customer);
    user.save()

    admin = User(first_name='User',
                 last_name='Theuser',
                 birth_date=datetime.date.today(),
                 email='test1@email.com',
                 password='password').save()
    admin.roles.append(role_admin)
    admin.save()

    second_user = User(first_name='My User',
                       last_name='Van Gogh',
                       birth_date=datetime.date.today(),
                       email='test2@email.com',
                       password='password').save()
    second_user.roles.append(role_customer)


class UserEndpointsTest(TestCase):
    def create_app(self):
        init_app('user_service.tests.config')
        return app

    def setUp(self):
        create_database(self.app)

    def tearDown(self):
        os.remove(os.path.join(basedir, 'users.db'))

    def test_post_user(self):
        user = {'first_name': 'First',
                'last_name': 'Last',
                'birth_date': datetime.date.today().isoformat(),
                'email': 'test@email.com',
                'password': 'password'}

        json_user = json.dumps(user)
        response = self.client.post('/api/users', data=json_user, content_type='application/json')
        self.assertStatus(response, 201)
        self.assertIsNotNone(response.json['id'])

    def test_get_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password')
        user.save()
        response = self.client.get('/api/users/'+str(user.id))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['first_name'], 'First')

    def test_put_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password')
        user.save()
        user.first_name = 'UpdateFirstName'
        response = self.client.put('/api/users/'+str(user.id), data=json.dumps(user.to_dict()), content_type='application/json')
        self.assertStatus(response, 200)
        self.assertEqual(response.json['first_name'], 'UpdateFirstName')

    def test_post_user_integrity_check(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password')
        user.save()
        user_ = {'first_name': 'First',
                 'last_name': 'Last',
                 'birth_date': datetime.date.today().isoformat(),
                 'email': 'test@email.com',
                 'password': 'password'}

        json_user = json.dumps(user_)
        response = self.client.post('/api/users', data=json_user, content_type='application/json')
        self.assert400(response)

    def test_delete_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password')
        user.save()
        response = self.client.delete('/api/users/'+str(user.id))
        self.assertStatus(response, 204)

    def test_search_users(self):
        create_users_and_roles()
        filters = [dict(name='first_name', op='like', val='First')]
        response = self.client.get('/api/users?q=%s' % json.dumps(dict(filters=filters)))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['num_results'], 1)
        filters = [dict(name='first_name', op='like', val='%User%')]
        response = self.client.get('/api/users?q=%s' % json.dumps(dict(filters=filters)))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['num_results'], 2)
        filters = [dict(name='first_name', op='like', val='%Nouser%')]
        response = self.client.get('/api/users?q=%s' % json.dumps(dict(filters=filters)))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['num_results'], 0)

    def test_login_logout_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password')
        user.save()
        user_ = {'email': 'test@email.com',
                 'password': 'password'}

        json_user = json.dumps(user_)
        response = self.client.post('/users/login', data=json_user, content_type='application/json')
        self.assertStatus(response, 200)
        self.assertEqual(1, response.json['login_count'])

        response = self.client.post('/users/logout', data=json.dumps({'user_id': response.json['id']}),
                                    content_type='application/json')
        self.assertStatus(response, 200)
        self.assertEqual('OK', response.json['status'])


    def test_login_user_not_found(self):
        user_ = {'email': 'test111@email.com',
                 'password': 'password'}

        json_user = json.dumps(user_)
        response = self.client.post('/users/login', data=json_user, content_type='application/json')
        self.assertStatus(response, 404)