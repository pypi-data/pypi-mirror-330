# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Permission Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define a exceção `PermissionDeniedError`, que é utilizada para indicar falhas de autenticação de usuário.

Obs.:

- Segue os princípios da Clean Architecture ao separar claramente as exceções do domínio da aplicação.
- Aplica o princípio **Liskov Substitution Principle (LSP)**, pois a exceção `PermissionDeniedError` estende `DomainError`
  sem alterar seu comportamento esperado.

Author:           @diego.yosiura
Last Update:      27/02/2025 16:45
Created:          27/02/2025 16:45
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""

# Importa a classe base DomainError para definir exceções dentro do domínio da aplicação
from . import DomainError


class PermissionDeniedError(DomainError):
    """
    Exceção que representa erro de permissão negada ao autenticar um usuário.

    Esta exceção deve ser lançada quando um usuário tenta acessar um recurso para o qual
    não tem permissão adequada.

    Herda de:
        DomainError: Classe base para erros do domínio da aplicação.

    Exemplo de uso:
        >>> raise PermissionDeniedError()

    """

    def __init__(self):
        """
        Inicializa a exceção com uma mensagem de erro padrão.

        O princípio **Open/Closed Principle (OCP)** é aplicado aqui, pois a classe pode ser
        estendida sem modificação, permitindo novas exceções específicas no futuro sem alterar este código.

        """
        # Chama o construtor da classe base com a mensagem de erro apropriada
        super().__init__("Permission Denied.")  # Mensagem fixa para indicar erro de permissão
