#!/usr/bin/env python
from . import app
from flask import json


@app.errorhandler(404)
def page_not_found(error):
    error_dict = {'status': 'error',
                  'code': 404,
                  'description': 'Element not found'}
    return json.dumps(error_dict), 404