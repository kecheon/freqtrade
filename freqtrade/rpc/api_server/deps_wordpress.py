import secrets
from typing import Dict, Tuple
import requests
from sqlalchemy.sql.sqltypes import Boolean

def verify_auth_from_wordpress_api(api_config, username: str, password: str):
  # authenticate from bitsbee.io api
  data = {
    "username": username,
    "password": password
  }
  return login_user(data)


def login_user(data: Dict[str, str]) -> Boolean:
        try:
            # fetch jwt from bitsbee.io API(wordpress jwt auth api)
            endpoint = 'https://bitsbee.io'
            params = {
                "rest_route": "/simple-jwt-login/v1/auth",
                "email": data.get('username'),
                "password": data.get('password')
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

