"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma interface para clientes API autenticados dentro do sistema SAGACE. 
A classe `APIClient` fornece uma estrutura base para requisições autenticadas, garantindo que qualquer implementação
específica siga um contrato comum.

Principais funcionalidades:

- Gerenciamento da URL base da API.
- Armazenamento e recuperação do token de autenticação.
- Definição de um método abstrato para requisições autenticadas.

Classes:

- ``APIClient``: Interface para clientes autenticados.

Exemplo de uso:

.. code-block:: python

    from sagace.infrastructure.api_client import APIClient
    from sagace.core import TokenStorage

    class MyAPIClient(APIClient):
        def request(self, method: str, endpoint: str, **kwargs):
            # Implementação específica da requisição
            pass

    api_client = MyAPIClient("https://api.sagace.online", TokenStorage())


Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:20
Criado em: 27/02/2025 16:20
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

from abc import ABC, abstractmethod

from . import TokenStorage


class APIClient(ABC):
    """
    Interface para clientes API autenticados.

    Esta classe serve como base para a implementação de clientes API que necessitam de autenticação.

    Princípios aplicados:

    - **Liskov Substitution (L - SOLID)**: Qualquer classe que herde de `APIClient` deve poder ser utilizada
      sem alterar o comportamento esperado.
    - **Dependency Inversion (D - SOLID)**: Depende da abstração de um armazenamento de tokens (`TokenStorage`).

    :param base_url: URL base da API.
    :type base_url: str
    :param token_storage: Instância responsável pelo armazenamento do token.
    :type token_storage: TokenStorage
    """

    def __init__(self, base_url: str, token_storage: TokenStorage):
        """
        Inicializa a classe APIClient.

        :param base_url: URL base da API.
        :type base_url: str
        :param token_storage: Instância responsável pelo armazenamento do token.
        :type token_storage: TokenStorage
        """

        # Remove qualquer barra extra no final da URL base para evitar problemas de formatação.
        self.base_url = base_url.rstrip("/")
        self.token_storage = token_storage

    @abstractmethod
    def request(self, method: str, endpoint: str, **kwargs):
        """
        Realiza uma requisição autenticada à API.

        Este método deve ser implementado pelas classes concretas que herdam de `APIClient`.

        :param method: Método HTTP a ser utilizado (GET, POST, etc.).
        :type method: str
        :param endpoint: Caminho do endpoint na API.
        :type endpoint: str
        :param kwargs: Parâmetros adicionais para a requisição.
        :return: Resposta da API.
        """
        pass