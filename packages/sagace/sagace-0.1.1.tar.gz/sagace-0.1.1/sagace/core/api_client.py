# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 16:20
    Created:          27/02/2025 16:20
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""

from abc import ABC, abstractmethod

from . import TokenStorage


class APIClient(ABC):
    """Interface para clientes API autenticados."""

    def __init__(self, base_url: str, token_storage: TokenStorage):
        self.base_url = base_url.rstrip("/")
        self.token_storage = token_storage

    @abstractmethod
    def request(self, method: str, endpoint: str, **kwargs):
        """Realiza uma requisição autenticada."""
        pass
