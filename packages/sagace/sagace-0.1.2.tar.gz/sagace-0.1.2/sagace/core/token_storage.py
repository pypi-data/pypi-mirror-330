# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 16:22
    Created:          27/02/2025 16:22
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
from abc import ABC, abstractmethod
from . import Token

class TokenStorage(ABC):
    """Interface para armazenar e recuperar tokens de autenticação."""

    @abstractmethod
    def save_token(self, token: Token):
        """Armazena o token."""
        pass

    @abstractmethod
    def get_token(self) -> Token:
        """Recupera o token armazenado."""
        pass
