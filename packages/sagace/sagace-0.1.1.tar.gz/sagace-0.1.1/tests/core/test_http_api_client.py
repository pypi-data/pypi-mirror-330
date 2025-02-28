import pytest
import requests
from unittest.mock import patch

from sagace.core.http_api_client import HTTPAPIClient
from sagace.core.storage.memory_storage import MemoryTokenStorage
from sagace.core import Token
from sagace.exceptions.domain.api_request_error import APIRequestError


def test_api_client_get_success():
    """Testa requisição GET bem-sucedida."""
    base_url = "https://demo.sagace.online/"
    token_storage = MemoryTokenStorage()
    token_storage.save_token(Token(base_url=base_url, access_token="TOKEN-JWT", description="", application_name=""))
    client = HTTPAPIClient(base_url, token_storage)

    mock_response = {"status": 1, "data": "Success"}

    with patch("requests.request") as mock_get:
        mock_get.return_value.status_code = 200  # Alterado para 200 em vez de 404
        mock_get.return_value.json.return_value = mock_response

        response = client.get("api/test")

        assert response["status"] == 1
        assert response["data"] == "Success"


def test_api_client_get_failure():
    """Testa erro na requisição GET."""
    base_url = "https://demo.sagace.online/"
    token_storage = MemoryTokenStorage()
    token_storage.save_token(Token(base_url=base_url, access_token="TOKEN-JWT", description="", application_name=""))
    client = HTTPAPIClient(base_url, token_storage)

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")

        with pytest.raises(APIRequestError):
            client.get("api/test")


def test_api_client_post_success():
    """Testa requisição POST bem-sucedida."""
    base_url = "https://demo.sagace.online/"
    token_storage = MemoryTokenStorage()
    token_storage.save_token(Token(base_url=base_url, access_token="TOKEN-JWT", description="", application_name=""))
    client = HTTPAPIClient(base_url, token_storage)

    mock_response = {"status": 1, "data": "Created"}

    with patch("requests.request") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response

        response = client.post("api/test", json={"key": "value"})

        assert response["status"] == 1
        assert response["data"] == "Created"


def test_api_client_post_failure():
    """Testa erro na requisição POST."""
    base_url = "https://demo.sagace.online/"
    token_storage = MemoryTokenStorage()
    token_storage.save_token(Token(base_url=base_url, access_token="TOKEN-JWT", description="", application_name=""))
    client = HTTPAPIClient(base_url, token_storage)

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")

        with pytest.raises(APIRequestError):
            client.post("api/test", json={"key": "value"})
