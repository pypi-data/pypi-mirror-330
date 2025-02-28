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
import json
from .. import Token
from .. import TokenStorage

class FileTokenStorage(TokenStorage):
    token_file:str

    def __init__(self, token_file: str):
        self.token_file = token_file

    """Armazena o token em um arquivo JSON."""

    def save_token(self, token: Token):
        with open(self.token_file, "w") as f:
            json.dump({
                "base_url": token.base_url,
                "access_token": token.access_token,
                "application_name": token.application_name,
                "description": token.description,
                "token_type": token.token_type
            }, f)

    def get_token(self) -> Token:
        try:
            with open(self.token_file, "r") as f:
                data = json.load(f)
                return Token(
                    base_url=data["base_url"],
                    access_token=data["access_token"],
                    application_name=data["application_name"],
                    description=data["description"],
                    token_type=data["token_type"]
                )
        except FileNotFoundError:
            raise ValueError("Token file not found.")
