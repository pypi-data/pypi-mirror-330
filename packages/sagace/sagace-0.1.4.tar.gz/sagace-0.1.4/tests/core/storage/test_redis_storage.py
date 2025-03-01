import pytest
from unittest.mock import MagicMock
from sagace.core.storage.redis_storage import RedisTokenStorage
from sagace.core import Token


@pytest.fixture
def redis_storage():
    """Cria uma instância mockada de RedisTokenStorage para testes."""
    mock_client = MagicMock()
    storage = RedisTokenStorage()
    storage.client = mock_client
    return storage


def test_save_and_get_token(redis_storage):
    """Testa se o token é salvo e recuperado corretamente no Redis mockado."""
    token = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-JWT", description="", application_name="")
    redis_storage.save_token(token)

    redis_storage.client.set.assert_any_call("base_url", "https://demo.sagace.online/")
    redis_storage.client.set.assert_any_call("access_token", "TOKEN-JWT")
    redis_storage.client.set.assert_any_call("application_name", "")
    redis_storage.client.set.assert_any_call("description", "")
    redis_storage.client.set.assert_any_call("token_type", "JWT")


def test_get_token_not_set(redis_storage):
    """Testa erro ao tentar recuperar um token quando nenhum foi salvo no Redis mockado."""
    redis_storage.client.get.return_value = None
    with pytest.raises(ValueError, match="Token not found in Redis"):
        redis_storage.get_token()


def test_overwrite_token(redis_storage):
    """Testa se um token salvo sobrescreve o anterior no Redis mockado."""
    token1 = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-OLD", description="",
                   application_name="")
    token2 = Token(base_url="https://demo.sagace.online/", access_token="TOKEN-NEW", description="",
                   application_name="")

    redis_storage.save_token(token1)
    redis_storage.save_token(token2)

    redis_storage.client.set.assert_any_call("access_token", "TOKEN-NEW")

