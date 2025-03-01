# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Token Expiration Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define a exceção `TokenExpiredError`, utilizada para indicar a expiração de um token de autenticação.

Obs.:

- Segue os princípios da **Clean Architecture**, separando a lógica de erro do domínio da aplicação.
- Aplica o princípio **Liskov Substitution Principle (LSP)**, pois `TokenExpiredError` estende `DomainError`
  sem modificar o comportamento esperado da classe base.

Author:           @diego.yosiura
Last Update:      27/02/2025 16:46
Created:          27/02/2025 16:46
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""

# Importa a classe base DomainError para definir exceções dentro do domínio da aplicação
from . import DomainError


class TokenExpiredError(DomainError):
    """
    Exceção que representa um erro de autenticação devido à expiração do token.

    Esta exceção deve ser lançada sempre que um token de autenticação não for mais válido,
    exigindo que o usuário obtenha um novo token antes de continuar.

    Herda de:
        DomainError: Classe base para erros do domínio da aplicação.

    Exemplo de uso:
        >>> raise TokenExpiredError()

    """

    def __init__(self):
        """
        Inicializa a exceção com uma mensagem de erro padrão.

        O princípio **Open/Closed Principle (OCP)** é aplicado aqui, pois a classe pode ser
        estendida no futuro para suportar diferentes tipos de erros relacionados à expiração
        de tokens sem modificar o código existente.
        """
        # Chama o construtor da classe base com a mensagem de erro apropriada
        super().__init__("Token Expired")  # Mensagem fixa indicando a expiração do token
