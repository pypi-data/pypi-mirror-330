# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Infrastructure Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define a exceção base `InfrastructureError`, utilizada para representar erros relacionados à infraestrutura.

Obs.:

- Segue os princípios da **Clean Architecture**, separando os erros de infraestrutura do domínio da aplicação.
- Aplica o princípio **Liskov Substitution Principle (LSP)**, pois outras exceções específicas podem herdar de `InfrastructureError`
  sem modificar seu comportamento esperado.

Author:           @diego.yosiura
Last Update:      27/02/2025 16:05
Created:          27/02/2025 16:05
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""


class InfrastructureError(Exception):
    """
    Exceção base para representar erros de infraestrutura.

    Esta classe deve ser utilizada como base para todas as exceções relacionadas à infraestrutura,
    como falhas de conexão, indisponibilidade de serviços e erros de comunicação com APIs externas.

    Herda de:
        Exception: Classe base de todas as exceções nativas do Python.

    Exemplo de uso:
        >>> raise InfrastructureError("Falha ao conectar ao banco de dados")

    """

    pass  # A classe serve apenas como uma base para outras exceções de infraestrutura
