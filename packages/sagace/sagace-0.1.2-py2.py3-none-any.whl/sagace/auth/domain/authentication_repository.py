# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 15:30
    Created:          27/02/2025 15:30
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
from ...core import Token, TokenStorage

from abc import ABC, abstractmethod


class AuthenticationRepository(ABC):
    """Interface para autenticação"""

    @abstractmethod
    def authenticate(self, base_url: str, username: str, password: str, application_token: str, token_storage: TokenStorage) -> Token:
        pass
