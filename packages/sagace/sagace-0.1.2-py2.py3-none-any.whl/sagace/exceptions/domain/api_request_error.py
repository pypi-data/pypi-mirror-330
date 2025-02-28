# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 16:46
    Created:          27/02/2025 16:46
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
from . import DomainError

class APIRequestError(DomainError):
    """Erro ao autenticar um usuário."""
    def __init__(self, status_code: int, error: str):
        super().__init__(f"API Request Error [{status_code}]: {error}.")