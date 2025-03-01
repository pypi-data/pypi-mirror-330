"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma estrutura para gerenciamento de tokens de autenticação dentro do sistema SAGACE.
A interface `TokenStorage` estabelece um contrato para armazenamento e recuperação de tokens de forma desacoplada,
permitindo diferentes implementações conforme a necessidade do sistema.

Principais funcionalidades:

- Definição de uma interface para armazenamento seguro de tokens de autenticação.
- Permite a implementação de diferentes estratégias de persistência (memória, arquivos, banco de dados, etc.).

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: Cada classe tem uma única responsabilidade clara.
- **Open/Closed Principle (OCP - SOLID)**: A interface `TokenStorage` pode ser estendida sem modificar seu código-fonte.
- **Dependency Inversion Principle (DIP - SOLID)**: `TokenStorage` define uma abstração para armazenamento de tokens,
  permitindo que implementações concretas sejam facilmente substituídas.

Classes:

- ``TokenStorage``: Interface abstrata para armazenar e recuperar tokens.

Exemplo de uso:

.. code-block:: python

    from sagace.core import Token, TokenStorage

    class MemoryTokenStorage(TokenStorage):
        # Implementação de TokenStorage que armazena o token em memória.
        def __init__(self):
            self._token = None

        def save_token(self, token: Token):
            self._token = token

        def get_token(self) -> Token:
            return self._token

    token_storage = MemoryTokenStorage()
    token = Token(
        base_url="https://api.sagace.online",
        access_token="abc123",
        application_name="Meu App",
        description="Token de acesso para integração."
    )
    token_storage.save_token(token)
    retrieved_token = token_storage.get_token()
    print(retrieved_token.get_auth_header())

Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:22
Criado em: 27/02/2025 16:22
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

from abc import ABC, abstractmethod
from . import Token


class TokenStorage(ABC):
    """
    Interface para armazenar e recuperar tokens de autenticação.

    Essa classe define um contrato para qualquer implementação de armazenamento de tokens,
    permitindo diferentes abordagens, como armazenamento em memória, arquivos ou banco de dados.

    Princípios aplicados:
    - **Dependency Inversion (D - SOLID)**: Permite substituir implementações sem modificar consumidores da interface.
    - **Open/Closed (O - SOLID)**: Pode ser estendida sem modificar o código existente.
    """

    @abstractmethod
    def save_token(self, token: Token):
        """
        Armazena o token de autenticação.

        :param token: Token a ser armazenado.
        :type token: Token
        """
        pass

    @abstractmethod
    def get_token(self) -> Token:
        """
        Recupera o token armazenado.

        :return: Instância do token armazenado.
        :rtype: Token
        """
        pass