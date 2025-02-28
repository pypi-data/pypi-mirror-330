"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo fornece um serviço de autenticação para facilitar o uso do sistema SAGACE.
A classe `AuthenticationService` encapsula a lógica de autenticação, delegando o processo
para a classe de caso de uso `AuthenticateUser`, que por sua vez utiliza `AuthenticationAPI`.

Principais funcionalidades:

- Abstrai a autenticação de usuários, simplificando a interface.
- Delegação do fluxo de autenticação conforme o princípio **Single Responsibility** (S - SOLID).
- Facilita a reutilização da lógica de autenticação em diferentes partes do sistema.

Classes:

- ``AuthenticationService``: Serviço de autenticação de usuários.

Exemplo de uso:

.. code-block:: python

    from sagace.application import AuthenticationService
    from sagace.core import TokenStorage

    service = AuthenticationService()
    token_storage = TokenStorage()
    token = service.login("https://api.sagace.online", "usuario", "senha", "app_token", token_storage)
    print(token)


Autor: Diego Yosiura
Última Atualização: 27/02/2025 15:32
Criado em: 27/02/2025 15:32
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

from ..infrastructure.authentication_api import AuthenticationAPI
from ..application import AuthenticateUser
from ...core import TokenStorage


class AuthenticationService:
    """
    Serviço de autenticação para facilitar o uso do sistema.

    Esta classe abstrai a autenticação de usuários, centralizando o fluxo em `AuthenticateUser`.
    Segue o princípio **Dependency Inversion (D - SOLID)**, garantindo que a implementação de
    autenticação possa ser alterada sem impactar os consumidores do serviço.
    """

    def __init__(self):
        """
        Inicializa o serviço de autenticação.

        O repositório de autenticação `AuthenticationAPI` é injetado na instância de `AuthenticateUser`,
        garantindo que qualquer mudança na lógica de autenticação possa ser realizada de forma desacoplada.

        Princípios aplicados:
        - **Dependency Inversion (D - SOLID)**: A classe depende de uma abstração, permitindo substituição.
        - **Single Responsibility (S - SOLID)**: Centraliza a autenticação sem lidar com detalhes internos da API.
        """
        self.use_case = AuthenticateUser(auth_repository=AuthenticationAPI())

    def login(self, base_url: str, username: str, password: str, application_token: str,
              token_storage: TokenStorage) -> str:
        """
        Realiza login e retorna o token JWT.

        :param base_url: URL base da API de autenticação.
        :type base_url: str
        :param username: Nome de usuário para autenticação.
        :type username: str
        :param password: Senha do usuário.
        :type password: str
        :param application_token: Token da aplicação para autenticação.
        :type application_token: str
        :param token_storage: Instância responsável por armazenar o token JWT.
        :type token_storage: TokenStorage
        :return: Token de autenticação JWT.
        :rtype: str
        """

        # Chama a camada de aplicação para realizar a autenticação
        token = self.use_case.execute(base_url, username, password, application_token, token_storage)

        # Retorna apenas o token de acesso
        return token.access_token
