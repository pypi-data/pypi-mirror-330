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


from ..domain import AuthenticationRepository
from ...core import Token, TokenStorage

class AuthenticateUser:
    """
    Caso de uso para autenticação de usuário.

    Esta classe gerencia a autenticação de usuários utilizando um repositório de autenticação.

    Princípios aplicados:

    - **Single Responsibility (S - SOLID)**: A classe tem a única responsabilidade de gerenciar o processo de autenticação.
    - **Dependency Inversion (D - SOLID)**: Depende de uma abstração (``AuthenticationRepository``), permitindo diferentes
      implementações do repositório sem modificar esta classe.

    :param auth_repository: Repositório responsável pela autenticação.
    :type auth_repository: AuthenticationRepository
    """

    def __init__(self, auth_repository: AuthenticationRepository):
        """
        Inicializa a classe AuthenticateUser.

        :param auth_repository: Instância do repositório de autenticação.
        :type auth_repository: AuthenticationRepository
        """
        self.auth_repository = auth_repository

    def execute(self, base_url: str, username: str, password: str, application_token: str, token_storage: TokenStorage) -> Token:
        """
        Executa a autenticação e retorna o token JWT.

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

        # Chama o repositório de autenticação para validar as credenciais do usuário
        # Segue o princípio de Inversão de Dependência (D - SOLID), pois trabalha com uma abstração
        return self.auth_repository.authenticate(base_url, username, password, application_token, token_storage)
