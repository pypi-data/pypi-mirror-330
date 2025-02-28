# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 15:31
    Created:          27/02/2025 15:31
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
from ..domain import AuthenticationRepository
from ...core import TokenStorage, Token


class AuthenticateUser:
    """Caso de uso para autenticação de usuário"""

    def __init__(self, auth_repository: AuthenticationRepository):
        self.auth_repository = auth_repository

    def execute(self, base_url: str, username: str, password: str, application_token: str, token_storage: TokenStorage) -> Token:
        """Executa a autenticação e retorna o token JWT"""
        return self.auth_repository.authenticate(base_url, username, password, application_token, token_storage)
