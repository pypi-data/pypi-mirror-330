"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma estrutura para gerenciamento de tokens de autenticação dentro do sistema SAGACE.
A classe `MemoryTokenStorage` implementa a interface `TokenStorage` para armazenar tokens temporariamente na memória,
permitindo acesso rápido sem necessidade de persistência em arquivos ou banco de dados.

Principais funcionalidades:

- Armazena tokens de autenticação apenas em memória.
- Recupera tokens armazenados durante a execução do programa.
- Implementa a interface `TokenStorage`, garantindo flexibilidade e substituição de implementação.

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: A classe tem a única responsabilidade de armazenar tokens em memória.
- **Open/Closed Principle (OCP - SOLID)**: `MemoryTokenStorage` pode ser estendida sem modificar seu código-fonte.
- **Dependency Inversion Principle (DIP - SOLID)**: `MemoryTokenStorage` depende da abstração `TokenStorage`, permitindo flexibilidade.

Classes:

- ``MemoryTokenStorage``: Implementação concreta de `TokenStorage` utilizando armazenamento em memória.

Exemplo de uso:

.. code-block:: python

    from sagace.core import Token, MemoryTokenStorage

    token_storage = MemoryTokenStorage()
    token = Token(
        base_url="https://api.sagace.online",
        access_token="abc123",
        application_name="Meu App",
        description="Token de acesso temporário."
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

from .. import Token
from .. import TokenStorage


class MemoryTokenStorage(TokenStorage):
    """
    Implementação de `TokenStorage` para armazenamento temporário de tokens na memória.

    Esta classe permite armazenar tokens de autenticação em memória para acesso rápido,
    garantindo que os tokens sejam descartados ao final da execução do programa.

    Princípios aplicados:

    - **Single Responsibility Principle (S - SOLID)**: Responsável apenas por armazenar e recuperar tokens na memória.
    - **Dependency Inversion Principle (D - SOLID)**: Depende da abstração `TokenStorage`, garantindo desacoplamento.
    """

    def __init__(self):
        """
        Inicializa a classe `MemoryTokenStorage`, criando uma variável interna para armazenar o token.
        """
        self._token = None

    def save_token(self, token: Token):
        """
        Armazena o token na memória.

        :param token: Instância do token a ser armazenado.
        :type token: Token
        """
        self._token = token

    def get_token(self) -> Token:
        """
        Recupera o token armazenado na memória.

        :return: Instância do token armazenado.
        :rtype: Token
        :raises ValueError: Se o token não estiver armazenado na memória.
        """
        if not self._token:
            raise ValueError("Token not found in memory.")
        return self._token