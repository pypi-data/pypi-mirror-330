# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Interface Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define a exceção base `InterfaceError`, utilizada para representar erros na camada de interface.

Obs.:

- Segue os princípios da **Clean Architecture**, separando os erros da camada de interface do restante da aplicação.
- Aplica o princípio **Liskov Substitution Principle (LSP)**, pois outras exceções específicas podem herdar de `InterfaceError`
  sem modificar seu comportamento esperado.

Author:           @diego.yosiura
Last Update:      27/02/2025 16:04
Created:          27/02/2025 16:04
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""


class InterfaceError(Exception):
    """
    Exceção base para representar erros na camada de interface.

    Esta classe deve ser utilizada como base para todas as exceções relacionadas à interface,
    como falhas na comunicação entre diferentes camadas, problemas de entrada e saída de dados
    e interações inválidas.

    Herda de:
        Exception: Classe base de todas as exceções nativas do Python.

    Exemplo de uso:
        >>> raise InterfaceError("Erro na comunicação com o usuário")

    """

    pass  # A classe serve apenas como uma base para outras exceções relacionadas à interface
