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
from dataclasses import dataclass

@dataclass
class Token:
    base_url: str
    access_token: str
    application_name: str
    description: str
    token_type: str = "JWT"

    def get_auth_header(self) -> dict:
        """Retorna o cabeçalho de autenticação para requisições."""
        return {"Authorization": f"{self.token_type} {self.access_token}"}
