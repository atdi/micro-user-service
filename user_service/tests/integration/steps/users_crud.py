# coding: utf-8
from behave import given, when, then
import json
import requests
import datetime
from hamcrest import assert_that, equal_to


HOST = 'http://localhost:5000'


@given("Flask app is running")
def start_app(context):
    response = requests.get(HOST)
    assert response.status_code == 200



@when("We save a user")
def save_user(context):
    user = {'first_name': 'First',
            'last_name': 'Last',
            'birth_date': datetime.date.today().isoformat(),
            'email': 'test@email.com',
            'password': 'password',
            'phone': '48888'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/api/users', data=json_user, headers=headers)
    context.last_user_id = response.json()['id']
    assert_that(response.status_code, equal_to(201))


@then("We find the user")
def find_user(context):
    response = requests.get(HOST+'/api/users/'+context.last_user_id)
    assert_that(response.status_code, equal_to(200))
    assert_that(response.json()['first_name'], equal_to('First'))


@given("We have an user")
def we_have_an_user(context):
    user = {'first_name': 'First',
            'last_name': 'Last',
            'birth_date': datetime.date.today().isoformat(),
            'email': 'test2@email.com',
            'password': 'password',
            'phone': '48888'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/api/users', data=json_user, headers=headers)
    context.last_user_id = response.json()['id']
    assert_that(response.status_code, equal_to(201))


@when("We update the user")
def update_user(context):
    user = {'id': context.last_user_id,
            'first_name': 'UpdatedFirst',
            'last_name': 'Last',
            'birth_date': datetime.date.today().isoformat(),
            'email': 'test2@email.com',
            'password': 'password',
            'phone': '48888'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.put(HOST+'/api/users/'+context.last_user_id, data=json_user, headers=headers)
    assert_that(response.status_code, equal_to(200))


@then("The user is updated")
def check_update(context):
    response = requests.get(HOST+'/api/users/'+context.last_user_id)
    assert_that(response.status_code, equal_to(200))
    assert_that(response.json()['first_name'], equal_to('UpdatedFirst'))


@when("Submit login data")
def login_user(context):
    user = {'email': 'test@email.com',
            'password': 'password'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/api/users/login', data=json_user, headers=headers)
    context.response = response


@then("User is logged in")
def check_login(context):
    assert_that(context.response.status_code, equal_to(200))