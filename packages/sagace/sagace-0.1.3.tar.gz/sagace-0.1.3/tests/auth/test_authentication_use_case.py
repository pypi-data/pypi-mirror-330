import pytest
from unittest.mock import patch, MagicMock

from sagace.auth.application import AuthenticateUser
from sagace.auth.infrastructure.authentication_api import AuthenticationAPI
from sagace.exceptions.infrastructure.authentication_error import AuthenticationFailedError
from sagace.exceptions.domain.api_request_error import APIRequestError
from sagace.core import Token
from sagace.core.storage.memory_storage import MemoryTokenStorage


def test_authentication_use_case_success():
    """Testa o caso de uso de autenticação bem-sucedida."""
    auth_api = AuthenticationAPI()
    use_case = AuthenticateUser(auth_api)
    base_url = "https://demo.sagace.online/"
    username = "user@example.com"
    password = "securepassword"
    token_storage = MemoryTokenStorage()

    mock_response = Token(base_url=base_url, access_token="TOKEN-JWT", description="", application_name="")

    with patch.object(auth_api, 'authenticate', return_value=mock_response) as mock_auth:
        token = use_case.execute(base_url, username, password, "existing-token", token_storage)

        mock_auth.assert_called_once_with(base_url, username, password, "existing-token", token_storage)
        assert isinstance(token, Token)
        assert token.access_token == "TOKEN-JWT"


def test_authentication_use_case_invalid_credentials():
    """Testa erro de credenciais inválidas no caso de uso."""
    auth_api = AuthenticationAPI()
    use_case = AuthenticateUser(auth_api)
    base_url = "https://demo.sagace.online/"
    username = "wrong-user"
    password = "wrong-password"
    token_storage = MemoryTokenStorage()

    with patch.object(auth_api, 'authenticate', side_effect=AuthenticationFailedError()):
        with pytest.raises(AuthenticationFailedError):
            use_case.execute(base_url, username, password, "existing-token", token_storage)


def test_authentication_use_case_api_failure():
    """Testa erro genérico de falha na API no caso de uso."""
    auth_api = AuthenticationAPI()
    use_case = AuthenticateUser(auth_api)
    base_url = "https://demo.sagace.online/"
    username = "user@example.com"
    password = "securepassword"
    token_storage = MemoryTokenStorage()

    with patch.object(auth_api, 'authenticate', side_effect=APIRequestError(500, "Internal Server Error")):
        with pytest.raises(APIRequestError):
            use_case.execute(base_url, username, password, "existing-token", token_storage)
