"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo implementa a autenticação de usuários no sistema SAGACE, utilizando um repositório de autenticação
para verificação das credenciais e armazenamento do token de acesso.

Principais funcionalidades:

- Autenticação de usuários por meio de credenciais.
- Armazenamento do token JWT retornado pela API.
- Interface para diferentes métodos de armazenamento de tokens.

Classes:

- ``AuthenticateUser``: Classe responsável por gerenciar a autenticação de usuários.
- ``AuthenticationRepository``: Interface abstrata para repositórios de autenticação.

Exemplo de uso:

.. code-block:: python

    from sagace.auth import AuthenticateUser
    from sagace.domain import AuthenticationRepository
    from sagace.core import TokenStorage

    repo = AuthenticationRepository()
    token_storage = TokenStorage()
    auth = AuthenticateUser(repo)
    token = auth.execute("https://api.sagace.online", "usuario", "senha", "app_token", token_storage)
    print(token)

Autor:
    Diego Yosiura

Última Atualização:
    27/02/2025 15:31

Criado em:
    27/02/2025 15:31

Copyright:
    (c) Ampere Consultoria Ltda

Projeto Original:
    sagace-v2-package

IDE:
    PyCharm
"""

from ...core import Token, TokenStorage
from abc import ABC, abstractmethod

class AuthenticationRepository(ABC):
    """
    Interface abstrata para repositórios de autenticação.

    Esta interface define o contrato para qualquer classe que implemente um repositório
    de autenticação, garantindo a padronização do método de autenticação.

    Princípios aplicados:

    - **Dependency Inversion (D - SOLID)**: Depende de abstração para desacoplamento, garantindo flexibilidade
      na implementação sem afetar os consumidores dessa interface.
    """

    @abstractmethod
    def authenticate(self, base_url: str, username: str, password: str, application_token: str,
                     token_storage: TokenStorage) -> Token:
        """
        Autentica um usuário e retorna um token JWT.

        :param base_url: URL base da API de autenticação.
        :type base_url: str
        :param username: Nome de usuário para autenticação.
        :type username: str
        :param password: Senha do usuário.
        :type password: str
        :param application_token: Token da aplicação para autenticação.
        :type application_token: str
        :param token_storage: Objeto responsável por armazenar o token JWT.
        :type token_storage: TokenStorage
        :return: Token JWT retornado pela API.
        :rtype: Token
        """
        pass
