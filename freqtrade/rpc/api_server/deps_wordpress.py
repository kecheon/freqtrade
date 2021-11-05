import secrets
from typing import Dict, Tuple
import requests
from sqlalchemy.sql.sqltypes import Boolean
import os
import urllib.parse

def verify_auth_from_wordpress_api(api_config, username: str, password: str, request_url):
  # authenticate from bitsbee.io api
#  parsed_url = urllib.parse.urlparse(request_url)
#  if parsed_url.netloc != username.replace('@', 'at').replace('.', 'dot') + '.bitsbee.io':
#      return False
#  else:
    data = {
        "username": username,
        "password": password,
        "referrer": request_url
    }
    return login_user(data)


def login_user(data: Dict[str, str]) -> Boolean:
    # auth_key is disabled in bitsbee.io
    # auth_key_for_bitsbee = os.getenv('AUTH_KEY_BITSBEE')
    try:
        # fetch jwt from bitsbee.io API(wordpress jwt auth api)
        endpoint = 'https://api.bitsbee.io/auth/login'
        params = {
            "username": data.get('username'),
            "password": data.get('password'),
            "referrer": data.get('referrer')
        }

        res = requests.post(endpoint, json=params)
        try:
            data = res.json()
            if data['status'] == 'success':
                jwt = data['Authorization']
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'access_token': jwt
                }
                return True
            else:
                return False

        except:
            response_object = {
                'status': 'fail',
                'message': 'email or password does not match.'
            }
            return False
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }
        return False
