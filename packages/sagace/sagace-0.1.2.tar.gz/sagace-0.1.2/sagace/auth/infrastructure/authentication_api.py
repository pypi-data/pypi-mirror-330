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
import requests
from ..domain import AuthenticationRepository
from ...core import TokenStorage, Token
from ...exceptions.domain import APIRequestError
from ...exceptions.infrastructure import AuthenticationFailedError

class AuthenticationAPI(AuthenticationRepository):
    """Implementação da autenticação via API externa"""

    BASE_URL = "https://demo.sagace.online/"
    AUTH_URL = "auth/base/login/"

    def authenticate(self, base_url: str, username: str, password: str, token: str, token_storage: TokenStorage) -> Token:
        full_url = f"{base_url.rstrip('/')}/{self.AUTH_URL.lstrip('/')}"

        response = requests.post(
            url=full_url,
            json={"username": username, "password": password},
            headers={"Authorization": token}
        )

        try:
            response.raise_for_status()
        except Exception:
            raise APIRequestError(response.status_code, response.text)
        data = response.json()

        if 'data' not in data:
            raise AuthenticationFailedError()

        for item in ['ds_application_name', 'ds_description', 'authorization_token']:
            if item not in data['data']:
                raise AuthenticationFailedError()

        token = Token(
            base_url=base_url,
            application_name=data['data']["ds_application_name"],
            description=data['data']["ds_description"],
            access_token=data['data']["authorization_token"]
        )
        token_storage.save_token(token)
        return token
