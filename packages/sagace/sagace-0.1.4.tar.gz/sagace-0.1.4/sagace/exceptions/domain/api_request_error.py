"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define classes de exceções para tratamento de erros na camada de domínio do sistema SAGACE.
A classe `APIRequestError` representa erros de requisições feitas à API, garantindo um tratamento estruturado
para falhas durante chamadas externas.

Principais funcionalidades:

- Define uma exceção específica para falhas em requisições à API.
- Herdada de `DomainError`, garantindo consistência no tratamento de erros do domínio.

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: Cada classe tem uma única responsabilidade clara.
- **Open/Closed Principle (OCP - SOLID)**: `APIRequestError` pode ser estendida sem modificar seu código-fonte.
- **Encapsulamento**: Centraliza a manipulação de mensagens de erro dentro da exceção.

Classes:

- ``APIRequestError``: Representa erros em requisições à API.

Exemplo de uso:

.. code-block:: python

    from sagace.exceptions import APIRequestError

    try:
        raise APIRequestError(500, "Erro interno no servidor")
    except APIRequestError as e:
        print(f"Erro capturado: {e}")

Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:46
Criado em: 27/02/2025 16:46
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

from . import DomainError


class APIRequestError(DomainError):
    """
    Exceção para erros em requisições à API.

    Esta classe é usada para capturar erros retornados por chamadas de API, 
    fornecendo uma estrutura padronizada para tratamento dessas falhas.

    Princípios aplicados:
    - **Single Responsibility Principle (S - SOLID)**: Responsável apenas por representar erros de requisição à API.
    - **Encapsulamento**: Centraliza a manipulação das mensagens de erro.

    :param status_code: Código de status HTTP retornado pela API.
    :type status_code: int
    :param error: Mensagem de erro retornada pela API.
    :type error: str
    """

    def __init__(self, status_code: int, error: str):
        """
        Inicializa a exceção `APIRequestError`.

        :param status_code: Código de status HTTP retornado pela API.
        :type status_code: int
        :param error: Mensagem de erro retornada pela API.
        :type error: str
        """
        super().__init__(f"API Request Error [{status_code}]: {error}.")
