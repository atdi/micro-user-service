# coding: utf-8
from .models import User, Role
from flask import request, jsonify, abort
from user_service import app, rest_manager
from datetime import datetime

rest_manager.create_api(User, methods=['GET', 'POST', 'PUT', 'DELETE'])
rest_manager.create_api(Role, methods=['GET', 'POST'])


@app.route("/")
def index():
    return "OK"


@app.route("/users/login", methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        login_user(user)
        return jsonify(user.to_dict()), 200
    abort(404)


@app.route("/users/logout", methods=['POST'])
def logout():
    user_id = request.json['user_id']
    user = User.get_by_id(user_id)
    user.last_login_at = user.current_login_at
    user.current_login_at = None
    user.last_login_ip = user.current_login_ip
    user.current_login_ip = None
    user.save()
    return jsonify({'status': 'OK'})


def login_user(user):
    if 'X-Forwarded-For' not in request.headers:
        remote_addr = request.remote_addr or 'untrackable'
    else:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0]
    old_current_login, new_current_login = user.current_login_at, datetime.utcnow()
    old_current_ip, new_current_ip = user.current_login_ip, remote_addr

    user.last_login_at = old_current_login or new_current_login
    user.current_login_at = new_current_login
    user.last_login_ip = old_current_ip or new_current_ip
    user.current_login_ip = new_current_ip
    user.login_count = user.login_count + 1 if user.login_count else 1
    user.save()
