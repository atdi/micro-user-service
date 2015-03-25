# coding: utf-8

import os
import datetime
from sqlalchemy import create_engine
from flask import json
from flask_testing import TestCase
from user_service import init_app, app
from user_service.core import BaseModel
from user_service.tests.config import basedir
from user_service.models import User, Role, Country, Region, City, Customer

init_app('user_service.tests.config')
def create_database(test_app):
    engine = create_engine(test_app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    BaseModel.metadata.create_all(bind=engine)


def create_users_and_roles():
    role_customer = Role(name="CUSTOMER").save()
    role_admin = Role(name="ADMIN").save()

    user = User(first_name='First',
                last_name='Last',
                birth_date=datetime.date.today(),
                email='test@email.com',
                password='password',
                phone='4988888').save()

    user.roles.append(role_customer);
    user.save()

    admin = User(first_name='User',
                 last_name='Theuser',
                 birth_date=datetime.date.today(),
                 email='test1@email.com',
                 password='password',
                 phone='4988888').save()
    admin.roles.append(role_admin)
    admin.save()

    second_user = User(first_name='My User',
                       last_name='Van Gogh',
                       birth_date=datetime.date.today(),
                       email='test2@email.com',
                       password='password',
                       phone='4988888').save()
    second_user.roles.append(role_customer)


def create_cities():
    Country(id=1,
            code='RO',
            name='Romania').save()

    Region(id=1,
           code='BT',
           name='Botosani',
           country_id='1').save()

    Region(id=2,
           code='IS',
           name='Iasi',
           country_id='1').save()

    City(id=1,
         name='Botosani',
         region_id='1').save()

    City(id=2,
         name='Dorohoi',
         region_id='1').save()

    City(id=3,
         name='Iasi',
         region_id='2').save()


class UserServiceTestCase(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        create_database(self.app)

    def tearDown(self):
        os.remove(os.path.join(basedir, 'users.db'))


class UserEndpointsTest(UserServiceTestCase):

    def test_post_user(self):
        user = {'first_name': 'First',
                'last_name': 'Last',
                'birth_date': datetime.date.today().isoformat(),
                'email': 'test@email.com',
                'password': 'password',
                'phone': '4988888'}

        json_user = json.dumps(user)
        response = self.client.post('/api/users', data=json_user, content_type='application/json')
        self.assertStatus(response, 201)
        self.assertIsNotNone(response.json['id'])

    def test_get_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password',
                    phone='4988888')
        user.save()
        response = self.client.get('/api/users/'+str(user.id))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['first_name'], 'First')

    def test_put_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password',
                    phone='4988888')
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
                    password='password',
                    phone='4988888')
        user.save()
        user_ = {'first_name': 'First',
                 'last_name': 'Last',
                 'birth_date': datetime.date.today().isoformat(),
                 'email': 'test@email.com',
                 'password': 'password',
                 'phone': '4988888'}

        json_user = json.dumps(user_)
        response = self.client.post('/api/users', data=json_user, content_type='application/json')
        self.assert400(response)

    def test_delete_user(self):
        user = User(first_name='First',
                    last_name='Last',
                    birth_date=datetime.date.today(),
                    email='test@email.com',
                    password='password',
                    phone='4988888')
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
                    password='password',
                    phone='4988888')
        user.save()
        user_ = {'email': 'test@email.com',
                 'password': 'password'}

        json_user = json.dumps(user_)
        response = self.client.post('/api/users/login', data=json_user, content_type='application/json')
        self.assertStatus(response, 200)
        self.assertEqual(1, response.json['login_count'])

        response = self.client.post('/api/users/logout', data=json.dumps({'user_id': response.json['id']}),
                                    content_type='application/json')
        self.assertStatus(response, 200)
        self.assertEqual('OK', response.json['status'])

    def test_login_user_not_found(self):
        user_ = {'email': 'test111@email.com',
                 'password': 'password'}

        json_user = json.dumps(user_)
        response = self.client.post('/api/users/login', data=json_user, content_type='application/json')
        self.assertStatus(response, 404)
        self.assertEquals(404, response.json['code'])


class GeoEndpointsTest(UserServiceTestCase):

    def test_post_country_region_city(self):
        country = {'id': '1',
                   'code': 'DE',
                   'name': 'Germania'}
        json_country = json.dumps(country)
        response = self.client.post('/api/countries', data=json_country, content_type='application/json')
        self.assertStatus(response, 201)
        region = {'id': '1',
                  'code': 'B',
                  'name': 'Berlin',
                  'country_id': '1' }
        json_region = json.dumps(region)
        response = self.client.post('/api/regions', data=json_region, content_type='application/json')
        self.assertStatus(response, 201)
        city = {'id': '1',
                  'name': 'Berlin',
                  'region_id': '1' }
        json_city = json.dumps(city)
        response = self.client.post('/api/cities', data=json_city, content_type='application/json')
        self.assertStatus(response, 201)

    def test_get_regions_by_country_and_cities_by_region(self):
        create_cities()
        filters = [dict(name='country_id', op='eq', val='1')]
        response = self.client.get('/api/regions?q=%s' % json.dumps(dict(filters=filters)))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['num_results'], 2)
        filters = [dict(name='region_id', op='eq', val='1')]
        response = self.client.get('/api/cities?q=%s' % json.dumps(dict(filters=filters)))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['num_results'], 2)
        filters = [dict(name='region_id', op='eq', val='2')]
        response = self.client.get('/api/cities?q=%s' % json.dumps(dict(filters=filters)))
        self.assertStatus(response, 200)
        self.assertEqual(response.json['num_results'], 1)


class CustomerEndpointsTest(UserServiceTestCase):
    def test_add_customer(self):
        print("pass")
        """create_cities()
        customer = {"name": "Aurel Avramescu",
                    "type": "PF",
                    "unique_id": "1111111111",
                    "phone": "0788888",
                    "address": "Martirilor",
                    "city_id": "1" }
        json_customer = json.dumps(customer)
        response = self.client.post('/api/customers', data=json_customer, content_type='application/json')
        self.assertStatus(response, 201)
        self.assertEquals('Botosani', response.json['city']['name'])
        customer_id = response.json['id']
        address = {
            "contact_person": "Aurel Avramescu",
            "phone": "0722222",
            "address": "Berlin Adresa",
            "is_default": True,
            "customer_id": customer_id,
            "city_id": 1
        }
        json_address = json.dumps(address)
        response = self.client.post('/api/addresses', data=json_address, content_type='application/json')
        self.assertStatus(response, 201)
        address_id = response.json['id']
        response = self.client.get('/api/addresses/' + address_id)
        self.assert200(response)
        response = self.client.get('/api/customers/' + customer_id + '/address')
        self.assert200(response)
"""




