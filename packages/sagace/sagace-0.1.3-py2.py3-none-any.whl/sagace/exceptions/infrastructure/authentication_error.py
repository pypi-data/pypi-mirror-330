# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Authentication Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define a exceção `AuthenticationFailedError`, utilizada para indicar falhas no processo de autenticação.

Obs.:

- Segue os princípios da **Clean Architecture**, separando a lógica de erro do domínio da aplicação.
- Aplica o princípio **Liskov Substitution Principle (LSP)**, pois `AuthenticationFailedError` estende `InfrastructureError`
  sem modificar o comportamento esperado da classe base.

Author:           @diego.yosiura
Last Update:      27/02/2025 16:07
Created:          27/02/2025 16:07
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""

# Importa a classe base InfrastructureError para definir exceções relacionadas à infraestrutura
from . import InfrastructureError


class AuthenticationFailedError(InfrastructureError):
    """
    Exceção que representa uma falha no processo de autenticação de um usuário.

    Esta exceção deve ser lançada quando a autenticação falha devido a credenciais inválidas
    ou outros problemas que impeçam a autenticação bem-sucedida.

    Herda de:
        InfrastructureError: Classe base para erros de infraestrutura.

    Exemplo de uso:
        >>> raise AuthenticationFailedError()

    """

    def __init__(self):
        """
        Inicializa a exceção com uma mensagem de erro padrão.

        O princípio **Open/Closed Principle (OCP)** é aplicado aqui, pois a classe pode ser
        estendida no futuro para suportar diferentes tipos de falhas de autenticação sem
        modificar o código existente.
        """
        # Chama o construtor da classe base com a mensagem de erro apropriada
        super().__init__("Authentication process failed.")  # Mensagem fixa indicando falha na autenticação
