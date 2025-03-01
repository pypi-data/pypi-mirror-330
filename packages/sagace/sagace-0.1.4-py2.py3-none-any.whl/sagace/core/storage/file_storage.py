"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma estrutura para gerenciamento de tokens de autenticação dentro do sistema SAGACE.
A classe `FileTokenStorage` implementa a interface `TokenStorage` para armazenar tokens em um arquivo JSON,
permitindo a persistência do token mesmo após reinicializações do sistema.

Principais funcionalidades:

- Armazena tokens de autenticação em um arquivo JSON.
- Recupera tokens armazenados garantindo sua reutilização.
- Implementa a interface `TokenStorage`, garantindo flexibilidade e substituição de implementação.

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: A classe tem a única responsabilidade de armazenar tokens em arquivos.
- **Open/Closed Principle (OCP - SOLID)**: `FileTokenStorage` pode ser estendida sem modificar seu código-fonte.
- **Dependency Inversion Principle (DIP - SOLID)**: `FileTokenStorage` depende da abstração `TokenStorage`, permitindo flexibilidade.

Classes:
- ``FileTokenStorage``: Implementação concreta de `TokenStorage` utilizando arquivos JSON.

Exemplo de uso:

.. code-block:: python

    from sagace.core import Token, FileTokenStorage

    token_storage = FileTokenStorage("token.json")
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

import json
from .. import Token
from .. import TokenStorage


class FileTokenStorage(TokenStorage):
    """
    Implementação de `TokenStorage` para persistência de tokens em arquivos JSON.

    Esta classe permite armazenar tokens de autenticação em arquivos JSON para garantir sua persistência,
    garantindo que as credenciais sejam mantidas mesmo após reinicializações do sistema.

    Princípios aplicados:

    - **Single Responsibility Principle (S - SOLID)**: Responsável apenas por salvar e recuperar tokens de arquivos.
    - **Dependency Inversion Principle (D - SOLID)**: Depende da abstração `TokenStorage`, garantindo desacoplamento.

    :param token_file: Caminho do arquivo onde o token será armazenado.
    :type token_file: str
    """

    def __init__(self, token_file: str):
        """
        Inicializa a classe `FileTokenStorage` definindo o arquivo de armazenamento do token.

        :param token_file: Caminho do arquivo onde o token será armazenado.
        :type token_file: str
        """
        self.token_file = token_file

    def save_token(self, token: Token):
        """
        Armazena o token em um arquivo JSON.

        :param token: Instância do token a ser armazenado.
        :type token: Token
        """
        with open(self.token_file, "w") as f:
            json.dump({
                "base_url": token.base_url,
                "access_token": token.access_token,
                "application_name": token.application_name,
                "description": token.description,
                "token_type": token.token_type
            }, f)

    def get_token(self) -> Token:
        """
        Recupera o token armazenado no arquivo JSON.

        :return: Instância do token armazenado.
        :rtype: Token
        :raises ValueError: Se o arquivo de token não for encontrado.
        """
        try:
            with open(self.token_file, "r") as f:
                data = json.load(f)
                return Token(
                    base_url=data["base_url"],
                    access_token=data["access_token"],
                    application_name=data["application_name"],
                    description=data["description"],
                    token_type=data["token_type"]
                )
        except FileNotFoundError:
            raise ValueError("Token file not found.")
