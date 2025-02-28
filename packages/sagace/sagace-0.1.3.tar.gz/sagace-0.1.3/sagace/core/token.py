"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma estrutura para gerenciamento de tokens de autenticação dentro do sistema SAGACE.
A classe `Token` fornece um modelo estruturado para manipulação de tokens de acesso JWT.

Principais funcionalidades:

- Armazena e gerencia informações sobre o token JWT.
- Gera cabeçalhos de autenticação padronizados para requisições HTTP.

Classes:

- ``Token``: Representa um token de autenticação utilizado no sistema.

Exemplo de uso:

.. code-block:: python

    from sagace.core import Token

    token = Token(
        base_url="https://api.sagace.online",
        access_token="abc123",
        application_name="Meu App",
        description="Token de acesso para integração."
    )
    headers = token.get_auth_header()
    print(headers)

Autor: Diego Yosiura
Última Atualização: 27/02/2025 15:30
Criado em: 27/02/2025 15:30
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

from dataclasses import dataclass


@dataclass
class Token:
    """
    Representa um token de autenticação utilizado no sistema SAGACE.

    A classe `Token` encapsula informações sobre tokens JWT, garantindo que
    as requisições API possuam autenticação padronizada.

    Princípios aplicados:
    - **Single Responsibility (S - SOLID)**: A classe é responsável apenas pelo gerenciamento de tokens.
    - **Encapsulamento**: Centraliza o controle dos tokens dentro da aplicação.

    :param base_url: URL base da API autenticada.
    :type base_url: str
    :param access_token: Token de acesso JWT.
    :type access_token: str
    :param application_name: Nome da aplicação associada ao token.
    :type application_name: str
    :param description: Descrição do token.
    :type description: str
    :param token_type: Tipo do token (por padrão, JWT).
    :type token_type: str, optional
    """

    base_url: str
    access_token: str
    application_name: str
    description: str
    token_type: str = "JWT"

    def get_auth_header(self) -> dict:
        """
        Retorna um cabeçalho HTTP contendo o token de autenticação.

        Este método é utilizado para garantir que todas as requisições HTTP realizadas
        dentro do sistema incluam a autenticação necessária.

        :return: Dicionário contendo o cabeçalho de autorização.
        :rtype: dict
        """
        return {"Authorization": f"{self.token_type} {self.access_token}"}
