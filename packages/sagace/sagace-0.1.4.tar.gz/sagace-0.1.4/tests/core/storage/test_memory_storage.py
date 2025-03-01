import pytest
from sagace.core.storage.memory_storage import MemoryTokenStorage
from sagace.core import Token


@pytest.fixture
def memory_storage():
    """Cria uma instância de MemoryTokenStorage para testes."""
    return MemoryTokenStorage()


def test_save_and_get_token(memory_storage):
    """Testa se o token é salvo e recuperado corretamente na memória."""
    token = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-JWT", description="", application_name="")
    memory_storage.save_token(token)

    retrieved_token = memory_storage.get_token()

    assert isinstance(retrieved_token, Token)
    assert retrieved_token.access_token == "TOKEN-JWT"


def test_get_token_not_set(memory_storage):
    """Testa erro ao tentar recuperar um token quando nenhum foi salvo."""
    with pytest.raises(ValueError, match="Token not found in memory"):
        memory_storage.get_token()


def test_overwrite_token(memory_storage):
    """Testa se um token salvo sobrescreve o anterior."""
    token1 = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-OLD", description="",
                   application_name="")
    token2 = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-NEW", description="",
                   application_name="")

    memory_storage.save_token(token1)
    memory_storage.save_token(token2)

    retrieved_token = memory_storage.get_token()
    assert retrieved_token.access_token == "TOKEN-NEW"
