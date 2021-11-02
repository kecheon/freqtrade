from pdb import set_trace
from unittest.mock import MagicMock
import pytest
from requests.auth import _basic_auth_str
from starlette.testclient import TestClient
from freqtrade.loggers import setup_logging, setup_logging_pre
from freqtrade.rpc.api_server.webserver import ApiServer
from freqtrade.rpc.rpc import RPC
from freqtrade.state import RunMode
from tests.conftest import get_patched_freqtradebot
from tests.rpc.test_rpc_apiserver import BASE_URI, assert_response

_TEST_USER = 'test@gmail.com'
_TEST_PASS = 'test'

@pytest.fixture
def botclient(default_conf, mocker):
    setup_logging_pre()
    setup_logging(default_conf)
    default_conf['runmode'] = RunMode.DRY_RUN
    default_conf.update({"api_server": {"enabled": True,
                                        "listen_ip_address": "127.0.0.1",
                                        "listen_port": 8080,
                                        "CORS_origins": ['http://example.com'],
                                        "username": _TEST_USER,
                                        "password": _TEST_PASS,
                                        }})

    ftbot = get_patched_freqtradebot(mocker, default_conf)
    rpc = RPC(ftbot)
    mocker.patch('freqtrade.rpc.api_server.ApiServer.start_api', MagicMock())
    mocker.patch('freqtrade.rpc.api_server.deps_wordpress.verify_auth_from_wordpress_api', return_value='access_token')
    apiserver = ApiServer(rpc, default_conf)
    yield ftbot, TestClient(apiserver.app)
    # Cleanup ... ?

def test_wordpress_auth_api(botclient):
  ftbot, client = botclient
  rc = client.post(f"{BASE_URI}/token/login",
                     data=None,
                     headers={'Authorization': _basic_auth_str(_TEST_USER, _TEST_PASS),
                              'Origin': 'http://example.com'})
  assert_response(rc, 200)
  rc = client.post(f"{BASE_URI}/token/login",
                     data=None,
                     headers={'Authorization': _basic_auth_str('WRONG_USER', 'WRONG_PASS'),
                              'Origin': 'http://example.com'})
  assert_response(rc, 401)
  rc = client.post(f"{BASE_URI}/token/login",
                     data=None,
                     headers={'Authorization': _basic_auth_str(_TEST_USER, _TEST_PASS),
                              'Origin': 'http://another.com'})
  assert_response(rc, 401)

