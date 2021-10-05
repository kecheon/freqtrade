import secrets
from typing import Dict, Tuple
import requests
from sqlalchemy.sql.sqltypes import Boolean
import os
import urllib.parse

def verify_auth_from_wordpress_api(api_config, username: str, password: str, request_url):
  # authenticate from bitsbee.io api
  parsed_url = urllib.parse.urlparse(request_url)
  if parsed_url.netloc != username.replace('@', 'at').replace('.', 'dot') + '.bitsbee.io':
      return False
  else:
    data = {
        "username": username,
        "password": password
    }
    return login_user(data)


def login_user(data: Dict[str, str]) -> Boolean:
        auth_key_for_bitsbee = os.getenv('AUTH_KEY_BITSBEE')
        try:
            # fetch jwt from bitsbee.io API(wordpress jwt auth api)
            endpoint = 'https://bitsbee.io'
            params = {
                "rest_route": "/simple-jwt-login/v1/auth",
                "email": data.get('username'),
                "password": data.get('password'),
                "AUTH_KEY": auth_key_for_bitsbee
            }

            res = requests.post(endpoint, data=params)
            try:
                data = res.json()
                if data['success']:
                    jwt = data['data']['jwt']
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

