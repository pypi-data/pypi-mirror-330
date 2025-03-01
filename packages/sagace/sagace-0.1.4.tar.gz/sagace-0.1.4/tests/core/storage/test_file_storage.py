import pytest
import os
import json
from sagace.core.storage import FileTokenStorage
from sagace.core import Token

TOKEN_FILE = "test_token.json"


@pytest.fixture
def file_storage():
    """Cria uma instância de FileTokenStorage para testes."""
    storage = FileTokenStorage(TOKEN_FILE)
    yield storage
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def test_save_and_get_token(file_storage):
    """Testa se o token é salvo e recuperado corretamente."""
    token = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-JWT", description="", application_name="")
    file_storage.save_token(token)

    retrieved_token = file_storage.get_token()

    assert isinstance(retrieved_token, Token)
    assert retrieved_token.access_token == "TOKEN-JWT"


def test_get_token_file_not_found(file_storage):
    """Testa erro ao tentar recuperar um token quando o arquivo não existe."""
    with pytest.raises(ValueError, match="Token file not found"):
        file_storage.get_token()


def test_token_persistence(file_storage):
    """Testa se o token é realmente persistido no arquivo JSON."""
    token = Token(base_url="https://demo.sagace.online/", access_token="PERSISTED-TOKEN", description="",
                  application_name="")
    file_storage.save_token(token)

    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)

    assert data["access_token"] == "PERSISTED-TOKEN"