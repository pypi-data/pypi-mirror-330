"""Database client auth handler"""

import getpass
from functools import wraps
from pathlib import Path
from typing import Union, Optional
from os import environ

from requests.models import Response

from .connection import SessionConnect

TOKEN_FILE = '.seeqc-token.dat'


class Authorisation:
    """Client authentication"""

    def __init__(self,
                 url: Optional[str] = None,
                 refresh_path: Optional[str] = None,
                 ):
        self.access_token = None
        self.refresh_token = None
        self.refresh_path = None
        self.url = url
        if url is None:
            self.url = 'https://api.seeqc.cloud'
        self.set_refresh_path(refresh_path)
        self.session = SessionConnect(self.url)

    def initialise(self):
        """Create an authenticated session"""
        self._read_local_refresh_token()

    def send_password_reset_email(self, email: str):
        """Trigger password reset email send."""
        response = self.session.post('/api/v1/reset-password', data={'email': email})
        print(response.text)

    def set_refresh_path(self, refresh_path: Optional[str] = None):
        """Set the path for the refresh token from refresh_path or an env var"""
        if not refresh_path:
            token_var = environ.get('TOKEN_PATH')
            if not token_var:
                token_var = environ.get('SEEQC_TOKEN_PATH')
            if not token_var:
                token_var = './'
            self.refresh_path = Path(token_var) / TOKEN_FILE
            return self.refresh_path
        self.refresh_path = Path(refresh_path) / TOKEN_FILE
        return self.refresh_path

    def update_url(self, url: str):
        """Update API url attribute"""
        self.session.update_url(url)

    def authenticate(self, credentials=None) -> bool:
        """Prompt user to login and save tokens on success"""
        if credentials is None:
            credentials = self._get_credentials()
        status_code = self._authenticate(credentials=credentials)
        if status_code == 200:
            self._write_local_refresh_token()
            return True
        return False

    def _get_credentials(self) -> dict:
        """Prompt user credentials entry"""
        username = self._get_username()
        password = self._get_password()
        print('\nAuthenticating with authorisation server')
        return {'email': username, 'password': password}

    @staticmethod
    def _get_username() -> str:
        return input('Input your email address\n')

    @staticmethod
    def _get_password() -> str:
        return getpass.getpass('Input your password\n')

    def _authenticate(self, credentials: dict) -> int:
        """Exchange credentials for tokens"""
        response = self.session.post('/api/v1/authenticate',
                                     data=credentials)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens.get('access')
            self.refresh_token = tokens.get('refresh')
            self._construct_header()
            print('\nAuthentication successful')
        else:
            print('Invalid credentials received. Please try reinitialising the client')
        return response.status_code

    def refresh(self) -> bool:
        """Refresh the access token and retry on failure"""
        is_refreshed = self._is_valid_refresh_attempt()
        if is_refreshed:
            return True
        print('Refresh attempt failed')
        return False

    def _handle_successful_refresh_response(self, response: Response):
        """Update tokens if possible. Else prompt initialisation"""
        tokens = response.json()
        self.access_token = tokens.get('access')
        self.refresh_token = tokens.get('refresh')

    def _is_valid_refresh_attempt(self) -> bool:
        """Refresh access token and return boolean indication success"""
        response = self.session.post('/api/v1/refresh',
                                     data={'refresh': self.refresh_token})
        if response.status_code == 200:
            self._handle_successful_refresh_response(response)
            return True
        if response.status_code == 400:
            print('User session has expired or credentials invalid. Please enter your credentials')
            if self.authenticate():
                return True
        return False

    def _construct_header(self) -> dict:
        """Construct header in format for api gateway"""
        return {"Authorization": f"Bearer {self.access_token}"}

    def request_handler(self, request_function: callable) -> callable:
        """Decorator function for API calls. Discovers API url when not specified and constructs auth header"""
        @wraps(request_function)
        def decorated_fn(*args, **kwargs) -> Response:
            response = request_function(*args, **kwargs, headers=self._construct_header())
            response.close()
            if response.status_code == 401:
                if self.refresh():
                    response = request_function(*args, **kwargs, headers=self._construct_header())
                else:
                    print('Your authenticated session has expired and this client is unable to reauthenticate. '
                          'Please try reinstantiating the client.')
            return response
        return decorated_fn

    def _read_local_refresh_token(self):
        """Read in a local refresh token. Reauthenticate if none found."""
        try:
            token = self._get_local_token()
            if token is not None:
                self.refresh_token = token
                if not self.refresh():
                    self.authenticate()
            else:
                self.authenticate()
        except FileNotFoundError:
            self.authenticate()

    def _get_local_token(self) -> str:
        """Read in locally saved refresh token"""
        with open(self.refresh_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _write_local_refresh_token(self):
        """Write refresh token to the refresh path"""
        with open(self.refresh_path, 'w+', encoding='utf-8') as file:
            file.write(self.refresh_token)
