# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 16:24
    Created:          27/02/2025 16:24
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
from .. import Token
from .. import TokenStorage

class MemoryTokenStorage(TokenStorage):
    """Armazena o token apenas em memória."""

    def __init__(self):
        self._token = None

    def save_token(self, token: Token):
        self._token = token

    def get_token(self) -> Token:
        if not self._token:
            raise ValueError("Token not found in memory.")
        return self._token
