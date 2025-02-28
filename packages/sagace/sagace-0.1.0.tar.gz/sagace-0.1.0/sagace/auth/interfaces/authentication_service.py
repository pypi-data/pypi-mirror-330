# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 15:32
    Created:          27/02/2025 15:32
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
from ..infrastructure.authentication_api import AuthenticationAPI
from ..application import AuthenticateUser
from ...core import TokenStorage


class AuthenticationService:
    """Serviço de autenticação para facilitar o uso"""

    def __init__(self):
        self.use_case = AuthenticateUser(auth_repository=AuthenticationAPI())

    def login(self, base_url: str, username: str, password: str, application_token: str, token_storage: TokenStorage) -> str:
        """Realiza login e retorna o token JWT"""
        token = self.use_case.execute(base_url, username, password, application_token, token_storage)
        return token.access_token
