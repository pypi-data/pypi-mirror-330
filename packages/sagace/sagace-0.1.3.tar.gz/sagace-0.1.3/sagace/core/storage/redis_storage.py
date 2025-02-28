"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma estrutura para gerenciamento de tokens de autenticação dentro do sistema SAGACE.
A classe `RedisTokenStorage` implementa a interface `TokenStorage` para armazenar tokens em um banco Redis,
permitindo recuperação eficiente e persistente dos tokens.

Principais funcionalidades:

- Armazena tokens de autenticação no Redis.
- Recupera tokens armazenados garantindo sua reutilização.
- Implementa a interface `TokenStorage`, garantindo flexibilidade e substituição de implementação.

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: A classe tem a única responsabilidade de armazenar tokens no Redis.
- **Open/Closed Principle (OCP - SOLID)**: `RedisTokenStorage` pode ser estendida sem modificar seu código-fonte.
- **Dependency Inversion Principle (DIP - SOLID)**: `RedisTokenStorage` depende da abstração `TokenStorage`, permitindo flexibilidade.

Classes:

- ``RedisTokenStorage``: Implementação concreta de `TokenStorage` utilizando Redis.

Exemplo de uso:

.. code-block:: python

    from sagace.core import Token, RedisTokenStorage

    token_storage = RedisTokenStorage("redis://localhost:6379/0")
    token = Token(
        base_url="https://api.sagace.online",
        access_token="abc123",
        application_name="Meu App",
        description="Token de acesso persistente."
    )
    token_storage.save_token(token)
    retrieved_token = token_storage.get_token()
    print(retrieved_token.get_auth_header())

Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:24
Criado em: 27/02/2025 16:24
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

import redis
from .. import Token
from .. import TokenStorage


class RedisTokenStorage(TokenStorage):
    """
    Implementação de `TokenStorage` para persistência de tokens no Redis.

    Esta classe permite armazenar tokens de autenticação em Redis para garantir recuperação rápida
    e persistência, mesmo após a reinicialização do sistema.

    Princípios aplicados:

    - **Single Responsibility Principle (S - SOLID)**: Responsável apenas por salvar e recuperar tokens no Redis.
    - **Dependency Inversion Principle (D - SOLID)**: Depende da abstração `TokenStorage`, garantindo desacoplamento.

    :param redis_url: URL de conexão com o servidor Redis.
    :type redis_url: str
    """

    def __init__(self, redis_url="redis://localhost:6379/0"):
        """
        Inicializa a classe `RedisTokenStorage`, conectando ao Redis.

        :param redis_url: URL de conexão com o servidor Redis.
        :type redis_url: str
        """
        self.client = redis.StrictRedis.from_url(redis_url, decode_responses=True)

    def save_token(self, token: Token):
        """
        Armazena o token no Redis.

        :param token: Instância do token a ser armazenado.
        :type token: Token
        """
        self.client.set("base_url", token.base_url)
        self.client.set("access_token", token.access_token)
        self.client.set("application_name", token.application_name)
        self.client.set("description", token.description)
        self.client.set("token_type", token.token_type)

    def get_token(self) -> Token:
        """
        Recupera o token armazenado no Redis.

        :return: Instância do token armazenado.
        :rtype: Token
        :raises ValueError: Se o token não for encontrado no Redis.
        """
        base_url = self.client.get("base_url")
        access_token = self.client.get("access_token")
        application_name = self.client.get("application_name")
        description = self.client.get("description")
        token_type = self.client.get("token_type")

        if not access_token or not base_url:
            raise ValueError("Token not found in Redis.")
        return Token(
            base_url=base_url,
            access_token=access_token,
            application_name=application_name,
            description=description,
            token_type=token_type
        )
