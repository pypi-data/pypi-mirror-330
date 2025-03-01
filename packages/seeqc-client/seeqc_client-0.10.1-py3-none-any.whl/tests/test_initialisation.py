"""
Tests for the client authentication. Run locally as: pytest .\tests\test_initialisation.py
tmp_path_factory is a native pytest fixture used to create session scoped directories.
It is invoked as an OS specific pathlib object.
requests-mock is a fixture from the requests-mock pytest extension. It is used to register urls that when
accessed with a given method return a user configured requests Response object.
"""

# pylint: disable=redefined-outer-name, protected-access, unused-argument

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from requests.models import Response

from seeqc_client import Authorisation
from seeqc_client.authorisation import TOKEN_FILE

KEY = 'testkey'


@pytest.fixture(scope="session")
def local_token_file(tmp_path_factory):
    """Create a file to use as a mocked refresh token file"""
    directory = tmp_path_factory.mktemp("data")
    file = directory / TOKEN_FILE
    file.write_text(KEY, encoding='utf-8')
    return directory


@pytest.fixture
def valid_client(local_token_file):
    """Creates an Authorisation client with a path to a mocked refresh token"""
    with patch.dict(os.environ, {"TOKEN_PATH": str(local_token_file)}):
        return Authorisation()


@pytest.fixture
def refresh_200(requests_mock, valid_client):
    """Mocks the refresh route to return a 200 response containing tokens"""
    valid_credentials = {
        'access': 'access_token',
        'refresh': 'refresh_token'
    }
    credentials = json.dumps(valid_credentials)
    requests_mock.post(valid_client.url + '/api/v1/refresh',
                       status_code=200,
                       text=credentials)


def test_check_existing_token_exists(valid_client):
    """Read local refresh token. Checks same contents as that in local file"""
    client = valid_client
    token = client._get_local_token()
    assert token == KEY


def test_read_local_token_none_exists():
    """Read local refresh. Mocks token path env var. Assert file not found error"""
    with patch.dict(os.environ, {"TOKEN_PATH": 'badPath'}):
        client = Authorisation()
        with pytest.raises(FileNotFoundError):
            client._get_local_token()


def test_no_token_path():
    """Test that the refresh path must be set on client instantiation"""
    auth = Authorisation()
    auth.refresh_path = Path('./')


def test_authenticate_pass(valid_client, requests_mock):
    """Run the authenticate function but mock the requests to return a 200. Checks tokens updated"""
    client = valid_client
    access_token = 'test_access'
    refresh_token = 'test_refresh'
    valid_credentials = {
        'access': access_token,
        'refresh': refresh_token
    }
    credentials = json.dumps(valid_credentials)
    requests_mock.post('/api/v1/authenticate',
                       status_code=200,
                       text=credentials)
    credentials = {'data': 'data'}
    client._authenticate(credentials)
    assert client.refresh_token == valid_credentials.get('refresh')
    assert client.access_token == valid_credentials.get('access')


def test_authenticate_fail(valid_client, requests_mock):
    """Runs authenticate but mocks a none 200 response. Checks no tokens updated"""
    client = valid_client
    failed_status = 400
    requests_mock.post(client.url + '/api/v1/authenticate',
                       status_code=failed_status)
    credentials = {'data': 'data'}
    status = client._authenticate(credentials)
    assert client.refresh_token is None
    assert client.access_token is None
    assert status == failed_status


def test_get_credentials(valid_client):
    """Mock getting username and password and checks dictionary with credentials is returned"""
    with patch('seeqc_client.Authorisation._get_username') as mocked_user, \
            patch('seeqc_client.Authorisation._get_password') as mocked_password:
        password = 'pw'
        user = 'usr'
        mocked_password.return_value = password
        mocked_user.return_value = user
        credentials = valid_client._get_credentials()
        mocked_crendetials = {'email': user, 'password': password}
        assert credentials == mocked_crendetials


def test_set_refresh_path(valid_client):
    """Check refresh path can be updated with string"""
    new_dir = 'test'
    test_path = Path(new_dir) / TOKEN_FILE
    valid_client.set_refresh_path(new_dir)
    assert valid_client.refresh_path == test_path


def test_set_refresh_path_from_env_var(valid_client):
    """Mocks a token path env var, checks the refresh path contains this"""
    new_dir = 'tested'
    test_path = Path(new_dir) / TOKEN_FILE
    with patch.dict(os.environ, {"TOKEN_PATH": new_dir}):
        valid_client.set_refresh_path(None)
    assert valid_client.refresh_path == test_path


def test_try_refresh_pass(valid_client, refresh_200):
    """Test try refresh passes when refresh route returns a 200 response"""
    assert valid_client.refresh()


def test_try_refresh_fail(valid_client, requests_mock):
    """Test try refresh returns false when refresh route returns an error response"""
    requests_mock.post(valid_client.url + '/api/v1/refresh',
                       status_code=401)
    assert not valid_client.refresh()


def test_is_valid_refresh_attempt_200(valid_client, refresh_200):
    """Mock external response as a 200 and check returns True"""
    assert valid_client._is_valid_refresh_attempt()


def test_is_invalid_refresh_attempt_400(valid_client, requests_mock):
    """Mocks refresh response as a 400 and authentication failure"""
    requests_mock.post(valid_client.url + '/api/v1/refresh',
                       status_code=400)
    with patch('seeqc_client.Authorisation.authenticate') as mocked:
        mocked.return_value = False
        assert not valid_client._is_valid_refresh_attempt()
        mocked.assert_called()


def test_is_valid_refresh_attempt_400(valid_client, requests_mock):
    """Mocks refresh response as a 400 and authentication passes"""
    requests_mock.post(valid_client.url + '/api/v1/refresh',
                       status_code=400)
    with patch('seeqc_client.Authorisation.authenticate') as mocked:
        mocked.return_value = True
        assert valid_client._is_valid_refresh_attempt()
        mocked.assert_called()


def test_is_valid_refresh_attempt_invalid(valid_client, requests_mock):
    """Mock external response as a 500 and return False"""
    requests_mock.post(valid_client.url + '/api/v1/refresh',
                       status_code=500)
    assert not valid_client._is_valid_refresh_attempt()


def test_handle_successful_refresh_response(valid_client):
    """Given a response object containing tokens. Check relevant attributes are updated"""
    response = Response()
    access_token = 'test_access'
    refresh_token = 'test_refresh'
    valid_credentials = {
        'access': access_token,
        'refresh': refresh_token
    }
    credentials_string = json.dumps(valid_credentials)
    response_credentials = bytes(credentials_string, 'utf-8')
    response._content = response_credentials
    assert valid_client.refresh_token is None
    assert valid_client.access_token is None
    valid_client._handle_successful_refresh_response(response)
    assert valid_client.refresh_token == refresh_token
    assert valid_client.access_token == access_token


def test_request_handler_refresh_called_on_401(valid_client):
    """Test that when response returns failure that the tokens are refreshed"""
    @valid_client.request_handler
    def to_be_decorated(**kwargs):
        response = generic_mocked_response()
        response.status_code = 401
        return response
    with patch('seeqc_client.Authorisation.refresh') as mocked:
        mocked.return_value = True
        to_be_decorated()
        mocked.assert_called()


def generic_mocked_response():
    """A successful response with a passing close method"""
    def mocked_close():
        pass
    response = Response()
    response.status_code = 200
    response.close = mocked_close
    return response


def test_update_url(valid_client):
    """Test url attribute can be updated"""
    new_url = 'new_url'
    valid_client.update_url(new_url)
    assert valid_client.session.url == new_url
