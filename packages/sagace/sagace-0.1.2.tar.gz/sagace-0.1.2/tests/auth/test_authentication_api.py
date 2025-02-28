import pytest
import requests
from unittest.mock import patch

from sagace.auth.infrastructure.authentication_api import AuthenticationAPI
from sagace.exceptions.domain.api_request_error import APIRequestError
from sagace.exceptions.infrastructure.authentication_error import AuthenticationFailedError
from sagace.core import Token
from sagace.core.storage.memory_storage import MemoryTokenStorage


def test_authenticate_success():
    """Testa autenticação bem-sucedida."""
    auth_api = AuthenticationAPI()
    base_url = "https://demo.sagace.online/"
    username = "user@example.com"
    password = "securepassword"
    token_storage = MemoryTokenStorage()

    mock_response = {
        "status": 1,
        "code": 200,
        "message": "",
        "title": "base.messages.login_success",
        "data": {
            "ds_application_name": "NomeDaAplicacao",
            "ds_description": "Descrição completa do token",
            "authorization_token": "TOKEN-JWT"
        }
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        token = auth_api.authenticate(base_url, username, password, "existing-token", token_storage)

        assert isinstance(token, Token)
        assert token.access_token == "TOKEN-JWT"


def test_authenticate_invalid_credentials():
    """Testa erro de credenciais inválidas."""
    auth_api = AuthenticationAPI()
    base_url = "https://demo.sagace.online/"
    username = "wrong-user"
    password = "wrong-password"
    token_storage = MemoryTokenStorage()

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 401

        with pytest.raises(AuthenticationFailedError):
            auth_api.authenticate(base_url, username, password, "existing-token", token_storage)


def test_authenticate_token_expired():
    """Testa erro de token expirado."""
    auth_api = AuthenticationAPI()
    base_url = "https://demo.sagace.online/"
    username = "user@example.com"
    password = "securepassword"
    token_storage = MemoryTokenStorage()

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 403

        with pytest.raises(AuthenticationFailedError):
            auth_api.authenticate(base_url, username, password, "existing-token", token_storage)


def test_authenticate_api_failure():
    """Testa erro genérico de falha na API."""
    auth_api = AuthenticationAPI()
    base_url = "https://demo.sagace.online/"
    username = "user@example.com"
    password = "securepassword"
    token_storage = MemoryTokenStorage()

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")

        with pytest.raises(APIRequestError):
            auth_api.authenticate(base_url, username, password, "existing-token", token_storage)
